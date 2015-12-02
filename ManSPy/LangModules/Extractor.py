def Extract(version):
    return __import__('extractor_assocv'+str(version)).Extract
