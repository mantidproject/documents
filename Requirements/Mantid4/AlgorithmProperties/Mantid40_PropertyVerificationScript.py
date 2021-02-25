import re
import urllib2
import json
import math
from collections import Counter
from difflib import SequenceMatcher

class CompareStrings:
    WORD = re.compile(r'\w+')

    def _camel_case_split(self, identifier):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        sentence = ""
        for m in matches:
          sentence+=m.group(0)+" "
        return sentence

    def _get_cosine(self, vec1, vec2):
         intersection = set(vec1.keys()) & set(vec2.keys())
         numerator = sum([vec1[x] * vec2[x] for x in intersection])

         sum1 = sum([vec1[x]**2 for x in vec1.keys()])
         sum2 = sum([vec2[x]**2 for x in vec2.keys()])
         denominator = math.sqrt(sum1) * math.sqrt(sum2)

         if not denominator:
            return 0.0
         else:
            return float(numerator) / denominator

    def _text_to_vector(self, text):
         words = self.WORD.findall(text)
         return Counter(words)
        
    def _cosine_difference(self, sent1, sent2):
        return self._get_cosine(self._text_to_vector(sent1), self._text_to_vector(sent2))
        
    def getClosestMatches(self, string, list):
        filtList = [x for x in list if x != string and "Workspace" not in x]
        return [x for x in filtList if self._cosine_difference(self._camel_case_split(string), self._camel_case_split(x)) > 0.8]
        
class AlgorithmStats:
    algRecords = {}
    
    def __init__(self):
        #Thanks to Matt Jones' original script for this
        print "Retreiving algorithm statistics..."
        more = True
        pageNumber = 1
        while more:
            resp = urllib2.urlopen("http://reports.mantidproject.org/api/feature?page="+str(pageNumber)+"&format=json")
            more = self._parse(resp.read())
            pageNumber += 1
        
    def _parse(self, data_string):
        data = json.loads(data_string)
        
        for record in data['results']:
            if record['type'] == 'Algorithm':
                self.algRecords[record['name']] = record['count']
        
        return data['next'] is not None

    def getAlgorithmUsage(self, algName, algVersion):
        usage = None
        try: 
            usage = self.algRecords[algName+".v"+str(algVersion)]
        except:
            usage = 0
            
        return usage
        
class PropertyViolations:
    firstCapitalViolation = False
    inoutViolation = False
    illegalCharViolation = False
    camelCaseViolation = False
    indexPropertyUpdate = False
    
    def __init__(self, algName, algVersion, propertyName):
        self.algName = algName
        self.algVersion = algVersion
        self.propertyName = propertyName
        
    def setFirstCapitalViolation(self, set):
        self.firstCapitalViolation = set
        
    def setInoutViolation(self, set):
        self.inoutViolation = set
        
    def setIllegalCharViolation(self, set):
        self.illegalCharViolation = set
        
    def setCamelCaseViolation(self, set):
        self.camelCaseViolation = set
        
    def setIndexPropertyUpdate(self, set):
        self.indexPropertyUpdate = set
        
    def hasViolations(self):
        return self.illegalCharViolation | self.inoutViolation | self.firstCapitalViolation | self.camelCaseViolation | self.indexPropertyUpdate    
        
class AlgorithmPropertyValidator:
    # TODO this list should be empty
    PropertyWhiteList = {
    "CalculateUMatrix(v1)":("a", "b", "c", "alpha", "beta", "gamma"),
    "ConvertToMD(v1)":("dEAnalysisMode"),
    "ConvertToMDMinMaxLocal(v1)":("dEAnalysisMode"),
    "ConvertToMDMinMaxGlobal(v1)":("dEAnalysisMode"),
    "FindUBUsingLatticeParameters(v1)":("a", "b", "c", "alpha", "beta", "gamma"),
    "IndexSXPeaks(v1)":("a", "b", "c", "alpha", "beta", "gamma", "dTolerance"),
    "ModeratorTzero(v1)":("tolTOF"),
    "MuscatFunc(v1)":("dQ", "dW"),
    "OptimizeCrystalPlacement(v1)":("nPeaks", "nParams", "nIndexed"),
    "PDFFourierTransform(v1)":("rho0"),
    "PoldiAutoCorrelation(v5)":("wlenmin", "wlenmax"),
    "PoldiLoadChopperSlits(v1)":("nbLoadedSlits"),
    "PoldiLoadSpectra(v1)":("nbSpectraLoaded"),
    "PoldiProjectRun(v1)":("wlenmin", "wlenmax"),
    "PoldiRemoveDeadWires(v1)":("nbExcludedWires", "nbAuteDeadWires"),
    "SaveIsawQvector(v1)":("Qx_vector", "Qy_vector", "Qz_vector"),
    "SCDCalibratePanels(v1)":("a", "b", "c", "alpha", "beta", "gamma",
                              "useL0", "usetimeOffset", "usePanelWidth",
                              "usePanelHeight", "usePanelPosition",
                              "usePanelOrientation", "tolerance",
                              "MaxPositionChange_meters"),
    "SetSampleMaterial(v1)":("bAverage", "bSquaredAverage"),
    "SetUB(v1)":("a", "b", "c", "alpha", "beta", "gamma", "u", "v"),
    "ViewBOA(v1)":("CD-Distance"),
    "PoldiCreatePeaksFromCell(v1)":("a", "b", "c", "alpha", "beta", "gamma"),
    "CreateMD(v1)" : ("u", "v"),
    "AccumulateMD(v1)" : ("u", "v")
    }
    
    propertyViolations = []
    allAlgsProps = {}
    similarNames = {}
    usageStats = None
    comp = CompareStrings()
    
    def _camelCase(self, name):
        m = re.search("(?:[A-Z][a-z]+)+", name)
        if m is None:
            return True
        else:
            return False
            
    def _firstCapital(self, name):
        m = re.search('^[A-Z].*', name)
        if m is None:
            return True
        else:
            return False
            
    def _illegalCharacters(self, name):
        m = re.search('[\-\_\(\)\[\]]', name)
        if m is None:
            return False
        else:
            return True
            
    def _illegalWorkspaceType(self, prop):
        if prop.direction == kernel.Direction.InOut:
            return True
        else :
            return False
            
    def _similarPropertyName(self, allPropNames, propName):
        m = self.comp.getClosestMatches(propName, allPropNames)
        return m      
            
    def __extractPropNames(self, properties):
        return [prop.name for prop in properties]

    def __checkWhiteList(self, algName, algVersion, propName):
        whiteListed = False
        
        try:
            whiteListed = propName in self.PropertyWhiteList[algName+"(v"+str(algVersion)+")"]
        except:
            pass
            
        return whiteListed
        
    def _checkIndexProperty(self, prop):
        if any (type in prop.type for type in ("int list", "vector")): 
            keywords=("spectra", "spectrum", "index", "ids", "id", "detectorid")
            
            if any(keyword in prop.name.lower() for keyword in keywords):
                return True
            else:
                return False
        else:
            return False
            
    def _verifyAlgorithmProperties(self, algName, algVersion):     
        alg = AlgorithmManager.create(algName, algVersion)
        properties = alg.getProperties()
        allNames = self.__extractPropNames(properties)
        
        self.allAlgsProps[(algName, algVersion)] = allNames
        
        for prop in properties:
            if self.__checkWhiteList(algName, algVersion, prop.name):
                continue
                
            pv = PropertyViolations(algName, algVersion, prop.name)
                
            pv.setFirstCapitalViolation(self._firstCapital(prop.name))
            pv.setIllegalCharViolation(self._illegalCharacters(prop.name))
            pv.setCamelCaseViolation(self._camelCase(prop.name))
            pv.setIndexPropertyUpdate(self._checkIndexProperty(prop))
            
            if "Workspace" in prop.type:
                pv.setInoutViolation(self._illegalWorkspaceType(prop))
            
            if pv.hasViolations():
                self.propertyViolations.append(pv)
                
    def _populateNameClashes(self):
        print "Finding similar names..."
        while len(self.allAlgsProps):
            print len(self.allAlgsProps)
            alg, ver = next(iter(self.allAlgsProps))
            algProps = self.allAlgsProps.pop((alg, ver))
            
            for prop in algProps:
                for compAlgInfo, compProps in self.allAlgsProps.items():
                    compAlg, compVer = compAlgInfo
                    self.similarNames[(alg, ver, prop, compAlg, compVer)] = self._similarPropertyName(compProps, prop)              
        
    def _outputViolationCSV(self):
        print "Printing AlgorithmPropertyViolations.csv and InOutWorkspaceAlgorithms.txt..."
        with open("AlgorithmPropertyViolations.csv", "w") as csv, open("InOutWorkspaceAlgorithms.csv", "w") as inout:
            csv.write("Algorithm,Version,Property,First Capital Violation,Camel Case Violation,Illegal Characters,Index Property Update,Usage\n")
            inout.write("Algorithm,Usage\n")
            for v in self.propertyViolations:
                if v.hasViolations():
                    usage = self.usageStats.getAlgorithmUsage(v.algName, v.algVersion)
                    csv.write(v.algName+","+str(v.algVersion)+","+v.propertyName+
                              ","+str(v.firstCapitalViolation)+","+str(v.camelCaseViolation)+
                              ","+str(v.illegalCharViolation)+","+str(v.indexPropertyUpdate)+","+str(usage)+"\n")
                    if v.inoutViolation:
                        inout.write(v.algName+"v"+str(v.algVersion)+","+str(usage)+"\n")
        
                
    def _outputNameClashDocument(self):
        print "Printing possible name clashes in NameInconsistencies.csv"
        with open("PossibleNameDuplication.csv", "w") as clash:
            clash.write("Algorithm,Property Name,Clashing Algorithm, Possible Name Duplicates,usage\n")
            for info, clashNames in self.similarNames.items():
                algName, algVer, prop, clashAlg, clashAlgVer = info
                if len(clashNames):
                    clash.write(algName+"v"+str(algVer)+","+prop+","+clashAlg+"v"+str(clashAlgVer)+",");
                    for name in clashNames:
                        clash.write(name+" ")
                    usage = self.usageStats.getAlgorithmUsage(algName, algVer)
                    clash.write(","+str(usage)+"\n")
            
    def validateAllAlgorithms(self):
        algNames = AlgorithmFactory.getRegisteredAlgorithms(True)
        
        print "Validating algorithm property names..."
        for algName in algNames:
            algVersions = algNames[algName]
            for algVersion in algVersions:
                try:
                    self._verifyAlgorithmProperties(algName, algVersion)
                except Exception as e:
                    print e
                    print "Could not create " + algName
        self.usageStats = AlgorithmStats()   
        self._outputViolationCSV()
        self._populateNameClashes()
        self._outputNameClashDocument()
        
if __name__ == "__main__":
    validator = AlgorithmPropertyValidator()
    validator.validateAllAlgorithms()
