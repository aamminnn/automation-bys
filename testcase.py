import importlib

def import_module(version):
    module_name = f"script.{version}"
    return importlib.import_module(module_name)

versions = ['script','v3_7', 'v3_8', 'v3_9', 'v3_10', 'v3_11', 'v3_12', 'v3_13', 'v3_14','v3_15']
test_cases = {}

for version in versions:
    module = import_module(version)
    test_cases[version] = [
        module.OrganizationBasicData,
        module.RepoData,
        module.SampleBranch,  
        module.PullRequest,  
        module.LFSData, 
        module.Release,  
        module.Package, 
        module.Issue, 
        module.Project,
        module.Wiki, 
        module.Webhook, 
        module.OrganizationSecurityAlerts, 
        module.RepoCodeScanning,  
        module.RepoDependabot, 
        module.RepoSecretScanning, 
        module.Gist, 
        module.NewUser, 
        module.TestEmail, 
        module.ManagementConsoleSetting, 
    ]

# Accessing test cases
testcase = test_cases['script']
testcase3_7 = test_cases['v3_7']
testcase3_8 = test_cases['v3_8']
testcase3_9 = test_cases['v3_9']
testcase3_10 = test_cases['v3_10']
testcase3_11 = test_cases['v3_11']
testcase3_12 = test_cases['v3_12']
testcase3_13= test_cases['v3_13']
testcase3_14 = test_cases['v3_14']
testcase3_15 = test_cases['v3_15']

