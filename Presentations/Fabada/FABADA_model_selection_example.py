StartX = -0.54
EndX= +0.54

#-----------------------------------------------------------------------------------------------------------------------------

ws_data = mtd['iris56072_graphite002_Correct_56016_sqw']
ws_res = mtd['irs55878_graphite002_res']

chi_ws = WorkspaceFactory.Instance().create("Workspace2D",1,4,4)

L2='A1/3.14159265*(FWHM1/((x-c)^2+FWHM1^2))+A2/3.14159265*(FWHM2/((x-c)^2+FWHM2^2))'
L3= 'A1/3.14159265*(FWHM1/((x-c)^2+FWHM1^2))+A2/3.14159265*(FWHM2/((x-c)^2+FWHM2^2))+A3/3.14159265*(FWHM3/((x-c)^2+FWHM3^2))'
L4='A1/3.14159265*(FWHM1/((x-c)^2+FWHM1^2))+A2/3.14159265*(FWHM2/((x-c)^2+FWHM2^2))+A3/3.14159265*(FWHM3/((x-c)^2+FWHM3^2))+A4/3.14159265*(FWHM4/((x-c)^2+FWHM4^2))'


# ---------- FITTING delta + 2 Lorentzians ---------- 

function_str = "(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,Workspace=irs55878_graphite002_res,WorkspaceIndex=0;(name=DeltaFunction,Height=5;name=UserFunction,Formula="+L2+",A1=7.0,A2=9.0,FWHM1=0.3,FWHM2=0.01,c=0.001))"


minimizer_str="""FABADA,ChainLength=20000,StepsBetweenValues=10,ConvergenceCriteria=0.001,JumpAcceptanceRate=0.666667,
                         PDF=PDF_L2,Chains=Chains_L2,ConvergedChain=ConvergedChain_L2,
                            CostFunctionTable=CostFunctionTable_L2,Parameters=Parameters_L2"""


Fit(Function=function_str,InputWorkspace=ws_data,WorkspaceIndex=3,StartX=StartX,EndX=EndX,CreateOutput=True,
                Output='L2',OutputCompositeMembers=True,MaxIterations=50000,Minimizer=minimizer_str)
       
# ---------- FITTING delta + 3 Lorentzians ---------- 

function_str = "(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,Workspace=irs55878_graphite002_res,WorkspaceIndex=0;(name=DeltaFunction,Height=5;name=UserFunction,Formula="+L3+",A1=5.0,A2=10.0,A3=1.0,FWHM1=0.2,FWHM2=0.02,FWHM3=0.005,c=-0.0001))"

minimizer_str="""FABADA,ChainLength=20000,StepsBetweenValues=10,ConvergenceCriteria=0.001,JumpAcceptanceRate=0.666667,
                         PDF=PDF_L3,Chains=Chains_L3,ConvergedChain=ConvergedChain_L3,
                        CostFunctionTable=CostFunctionTable_L3,Parameters=Parameters_L3"""

Fit(Function=function_str,InputWorkspace=ws_data,WorkspaceIndex=3,StartX=StartX,EndX=EndX,CreateOutput=True,
                Output='L3',OutputCompositeMembers=True,MaxIterations=50000,Minimizer=minimizer_str)
                
# ---------- FITTING delta + 4 Lorentzians ----------                 
                
#function_str = "(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,Workspace=irs55878_graphite002_res,WorkspaceIndex=0;(name=DeltaFunction,Height=1;name=UserFunction,Formula="+L4+",A1=7.0,A2=1.0,A3=4.0,A4=5.0,FWHM1=0.3,FWHM2=0.005,FWHM3=0.06,FWHM4=0.04,c=0.001))"
function_str = "(composite=Convolution,FixResolution=true,NumDeriv=true;name=Resolution,Workspace=irs55878_graphite002_res,WorkspaceIndex=0;(name=DeltaFunction,Height=1;name=UserFunction,Formula="+L4+",A1=7.0,A2=1.0,A3=4.0,A4=5.0,FWHM1=0.3,FWHM2=0.005,FWHM3=0.06,FWHM4=0.04,c=0.001))"
minimizer_str="""FABADA,ChainLength=20000,StepsBetweenValues=10,ConvergenceCriteria=0.001,JumpAcceptanceRate=0.666667,
                         PDF=PDF_L4,Chains=Chains_L4,ConvergedChain=ConvergedChain_L4,
                        CostFunctionTable=CostFunctionTable_L4,Parameters=Parameters_L4"""

Fit(Function=function_str,InputWorkspace=ws_data,WorkspaceIndex=3,StartX=StartX,EndX=EndX,CreateOutput=True,
                Output='L4',OutputCompositeMembers=True,MaxIterations=50000,Minimizer=minimizer_str)
    
    

chi_ws.dataX(0)[0] = 0
chi_ws.dataY(0)[0] = 2140

chi2 = mtd['CostFunctionTable_L2']
chi_ws.dataX(0)[1] = 1
chi_ws.dataY(0)[1] = chi2.cell(0,1)

chi2 = mtd['CostFunctionTable_L3']
chi_ws.dataX(0)[2] = 2
chi_ws.dataY(0)[2] = chi2.cell(0,1)

chi2 = mtd['CostFunctionTable_L4']
chi_ws.dataX(0)[3] = 3
chi_ws.dataY(0)[3] = chi2.cell(0,1)
               


AnalysisDataService.Instance().add('Table_ChiMP', chi_ws)

