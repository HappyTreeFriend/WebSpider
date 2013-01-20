class Common(object):
    def test(self):
        pass
    def pdb(self):
        import pdb
        pdb.set_trace()
    def get_hash(self, str1):
        import hashlib
        return str(hashlib.md5(str(str1)).hexdigest())
    def site2db(self, str1):
        return str1.replace('.', '_')
    def db2site(self, str2):
        return str1.replace('_', '.')

comm = Common()
