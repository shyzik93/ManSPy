import importlib

def Extract(version):
    #return __import__('extractor_assocv'+str(version), globals={"__name__":__name__}, level=1).Extract
    return importlib.import_module('manspy.extractor_assocv' + str(version)).Extract
