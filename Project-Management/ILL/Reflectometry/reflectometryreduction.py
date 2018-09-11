import collections
import time
from mantid import mtd
from mantid.simpleapi import (ReflectometryILLConvertToQ, ReflectometryILLPolarizationCor,
                              ReflectometryILLPreprocess, ReflectometryILLSumForeground, RenameWorkspace, Scale,
                              Stitch1DMany)


class _SumType:
    def __init__(self, sumType):
        if sumType == 'SumInQ':
            self._sumInQ = True
        elif sumType == 'SumInLambda':
            self._sumInQ = False
        else:
            raise RuntimeError("Unknown SumType : {}. Options: 'SumInLambda', 'SumInQ'.".format(sumType))

    def inLambda(self):
        return not self._sumInQ

    def inQ(self):
        return self._sumInQ

    def __repr__(self):
        return 'SumInQ' if self._sumInQ else 'SumInLambda'


class _CommonSettings:
    def __init__(self, sumType, polarizationEffFile, finalScaling):
        self.polarizationEffFile = polarizationEffFile
        self.scaling = finalScaling
        self.sumType = _SumType(sumType)
        self.polarized = polarizationEffFile is not None


class Background:
    def __init__(self, width, offset):
        self.width = width
        self.offset = offset


class Foreground:
    def __init__(self, lowAngleWidth, highAngleWidth, directCentre=None, reflectedCentre=None):
        self.lowAngleWidth = lowAngleWidth
        self.highAngleWidth = highAngleWidth
        self.directCentre = directCentre
        self.reflectedCentre = reflectedCentre

    def halfWidths(self):
        return [self.lowAngleWidth, self.highAngleWidth]


class Setup:
    def __init__(self, label, direct, reflecteds, foreground, twoTheta, lowAngleBkg, highAngleBkg,
                 wavelengthRange, groupingQFraction, flatSample, commonSettings):
        self.label = label
        self._commonSettings = commonSettings
        self._direct = direct
        if isinstance(reflecteds, str) or not isinstance(reflecteds, collections.Iterable):
            reflecteds = [reflecteds]
        self._reflecteds = reflecteds
        self._foreground = foreground
        self._twoTheta = twoTheta
        self._lowAngleBkg = lowAngleBkg
        self._workspaceNamesForQConversion = ['reflected-{}-foreground-{}'.format(reflecteds[0], label)]
        self._workspaceNamesForStitching = list()
        self._highAngleBkg = highAngleBkg
        self._wavelengthRange = wavelengthRange
        self._groupingQFraction = groupingQFraction
        self._flatSample = flatSample

    def directPreprocessProperties(self):
        props = {
            'Run': self._direct,
            'OutputWorkspace': 'direct-{}-{}'.format(self._direct, self.label),
            'OutputBeamPositionWorkspace': 'direct-{}-beam-position-{}'.format(self._direct, self.label),
            'ForegroundHalfWidth': self._foreground.halfWidths(),
            'SlitNormalisation': 'Slit Normalisation ON'
        }
        beamPosition = self._foreground.directCentre
        if beamPosition is not None:
            props['BeamPosition'] = beamPosition
        bkgLowAngle = self._lowAngleBkg
        if bkgLowAngle is not None:
            props['LowAngleBkgOffset'] = bkgLowAngle.offset
            props['LowAngleBkgWidth'] = bkgLowAngle.width
        bkgHighAngle = self._highAngleBkg
        if bkgHighAngle is not None:
            props['HighAngleBkgOffset'] = bkgHighAngle.offset
            props['HighAngleBkgWidth'] = bkgHighAngle.width
        return props

    def directSumForegroundProperties(self):
        props = {
            'InputWorkspace': 'direct-{}-{}'.format(self._direct, self.label),
            'OutputWorkspace': 'direct-{}-foreground-{}'.format(self._direct, self.label)
        }
        if self._commonSettings.sumType.inLambda():
            wavelengthRange = self._wavelengthRange
            if wavelengthRange is not None:
                props['WavelengthRange'] = wavelengthRange
        return props

    def directPolarizationCorProperties(self):
        props = {
            'InputWorkspaces': 'direct-{}-foreground-{}'.format(self._direct, self.label),
            'OutputWorkspace': 'direct-{}-polcor-{}'.format(self._direct, self.label),
            'EfficiencyFile': self._commonSettings.polarizationEffFile
        }
        return props

    def isDirectCached(self):
        workspaces = mtd.getObjectNames()
        name = 'direct-{}-foreground-{}'.format(self._direct, self.label)
        return name in workspaces

    def isPolarized(self):
        return self._commonSettings.polarized

    def reflectedConvertToQProperties(self):
        propertyList = list()
        for wsName in self._workspaceNamesForQConversion:
            outputWSName = '{}-reflectivity'.format(wsName)
            props = {
                'InputWorkspace': wsName,
                'OutputWorkspace': outputWSName,
                'ReflectedBeamWorkspace': '{}-{}'.format(self._reflecteds[0], self.label),
                'DirectBeamWorkspace': 'direct-{}-{}'.format(self._direct, self.label),
                'Polarized': self._commonSettings.polarized,
            }
            if self._commonSettings.sumType.inLambda():
                props['DirectForegroundWorkspace'] = 'direct-{}-foreground-{}'.format(self._direct, self.label)
            groupingQ = self._groupingQFraction
            if groupingQ is not None:
                props['GroupingQFraction'] = groupingQ
            propertyList.append(props)
            self._workspaceNamesForStitching.append(outputWSName)
        return propertyList

    def reflectedPolarizationCorProperties(self):
        inputWorkspaces = ''
        separator = ''
        for r in self._reflecteds:
            inputWorkspaces += separator + 'reflected-{}-foreground-{}'.format(r, self.label)
            separator = ','
        props = {
            'InputWorkspaces': inputWorkspaces,
            'OutputWorkspace': 'reflected-polcor-{}'.format(self.label),
            'EfficiencyFile': self._commonSettings.polarizationEffFile
        }
        return props

    def reflectedPreprocessProperties(self):
        propertyList = list()
        for r in self._reflecteds:
            props = {
                'Run': r,
                'OutputWorkspace': '{}-{}'.format(r, self.label),
                'ForegroundHalfWidth': self._foreground.halfWidths(),
                'SlitNormalisation': 'Slit Normalisation ON',
                'SubalgorithmLogging': 'Logging ON'
            }
            beamCentre = self._foreground.reflectedCentre
            if beamCentre is not None:
                props['BeamCentre'] = beamCentre            
            twoTheta = self._twoTheta
            if twoTheta is not None:
                props['BraggAngle'] = twoTheta
            else:
                props['DirectBeamPositionWorkspace'] = 'direct-{}-beam-position-{}'.format(self._direct, self.label)
            bkgLowAngle = self._lowAngleBkg
            if bkgLowAngle is not None:
                props['LowAngleBkgOffset'] = bkgLowAngle.offset
                props['LowAngleBkgWidth'] = bkgLowAngle.width
            bkgHighAngle = self._highAngleBkg
            if bkgHighAngle is not None:
                props['HighAngleBkgOffset'] = bkgHighAngle.offset
                props['HighAngleBkgWidth'] = bkgHighAngle.width
            propertyList.append(props)
        return propertyList

    def reflectedSumForegroundProperties(self):
        propertyList = list()
        for r in self._reflecteds:
            props = {
                'InputWorkspace': '{}-{}'.format(r, self.label),
                'OutputWorkspace': 'reflected-{}-foreground-{}'.format(r, self.label),
                'SummationType': str(self._commonSettings.sumType),
                'DirectForegroundWorkspace': 'direct-{}-foreground-{}'.format(self._direct, self.label)
            }
            wavelengthRange = self._wavelengthRange
            if wavelengthRange is not None:
                props['WavelengthRange'] = wavelengthRange
            propertyList.append(props)
            if self._commonSettings.sumType.inQ():
                props['FlatSample'] = 'Flat Sample' if self._flatSample else 'Bent Sample'
        return propertyList

    def stitchableWorkspaceNames(self):
        return self._workspaceNamesForStitching

    def updatePolarizedWorkspaces(self):
        polCorGroup = mtd['reflected-polcor-{}'.format(self.label)]
        self._workspaceNamesForQConversion = polCorGroup.getNames()


class Reduction:
    def __init__(self, title, sumType='SumInLambda', polarizationEffFile=None, finalScaling=1.0):
        self.clock = time.time()
        self.setups = list()
        self.title = title
        self._commonSettings = _CommonSettings(sumType, polarizationEffFile, finalScaling)

    def add(self, direct, reflected, foreground, twoTheta=None, lowAngleBkg=None, highAngleBkg=None, 
            wavelengthRange=None, groupingQFraction=None, flatSample=True, label=None):
        if label is None:
            if twoTheta is None or isinstance(twoTheta, str):
                label = len(self.setups) + 1
            else:
                label = twoTheta
        setup = Setup(label, direct, reflected, foreground, twoTheta, lowAngleBkg, highAngleBkg,
                      wavelengthRange, groupingQFraction, flatSample, self._commonSettings)
        self.setups.append(setup)

    def finalScalingProperties(self):
        factor = self._commonSettings.scaling
        if factor != 1.:
            props = {
                'InputWorkspace': '{}'.format(self.title),
                'OutputWorkspace': '{}'.format(self.title),
                'Factor': factor
            }
            return props
        else:
            return dict()

    def renameProperties(self):
        if len(self.setups) == 1:
            propertyList = list()
            wsNames = self.setups[0].stitchableWorkspaceNames()
            for name in wsNames:
                suffix = self._findPolarizationSuffix(name)
                props = {
                    'InputWorkspace': '{}'.format(name),
                    'OutputWorkspace': '{}'.format(self.title) + suffix
                }
                propertyList.append(props)
            return propertyList
        else:
            return list()

    def sumType(self):
        return self._commonSettings.sumType

    def stitchingProperties(self):
        if len(self.setups) > 1:
            propertyList = list()
            setupWSList = list()
            for setup in self.setups:
                setupWSList.append(setup.stitchableWorkspaceNames())
            stitchList = list()
            for i in range(len(setupWSList[0])):
                wsList = list()
                for j in range(len(setupWSList)):
                    wsList.append(setupWSList[j][i])
                stitchList.append(wsList)
            for names in stitchList:
                inputWorkspaces = ''
                separator = ''
                for name in names:
                    inputWorkspaces += separator + name
                    separator = ','
                suffix = self._findPolarizationSuffix(name)
                props = {
                    'InputWorkspaces': inputWorkspaces,
                    'OutputWorkspace': '{}'.format(self.title) + suffix
                }
                propertyList.append(props)
            return propertyList
        else:
            return list()

    def _findPolarizationSuffix(self, s):
        for suffix in ['_--', '_-+', '_+-', '_++']:
            if suffix in s:
                return suffix
        return ''


def reduce(reductions):
    if not isinstance(reductions, collections.Iterable):
        reductions = [reductions]
    for reduction in reductions:
        for setup in reduction.setups:
            if not setup.isDirectCached():
                # Process direct
                properties = setup.directPreprocessProperties()
                ReflectometryILLPreprocess(**properties)
                properties = setup.directSumForegroundProperties()
                ReflectometryILLSumForeground(**properties)
            if setup.isPolarized():
                properties = setup.directPolarizationCorProperties()
                ReflectometryILLPolarizationCor(**properties)
            # Process reflected
            for properties in setup.reflectedPreprocessProperties():
                ReflectometryILLPreprocess(**properties)
            for properties in setup.reflectedSumForegroundProperties():
                ReflectometryILLSumForeground(**properties)
            if setup.isPolarized():
                properties = setup.reflectedPolarizationCorProperties()
                ReflectometryILLPolarizationCor(**properties)
                setup.updatePolarizedWorkspaces()
            for properties in setup.reflectedConvertToQProperties():
                ReflectometryILLConvertToQ(**properties)
        for properties in reduction.stitchingProperties():
            result = Stitch1DMany(**properties)
        for properties in reduction.renameProperties():
            # If there is nothing to stitch, we just rename.
            RenameWorkspace(**properties)
        properties = reduction.finalScalingProperties()
        if properties:
            Scale(**properties)
        finishTime = time.time()
        print("'{}' processed in {:.2} seconds".format(reduction.title, finishTime - reduction.clock))
