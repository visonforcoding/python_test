from tornado.options import define,options
define('env',default='vison')
class Env:

    SERVER_PORT = 8888

    DB_MDB_HOST = {'prd':'','vison':'192.168.33.10'}
    DB_MDB_PORT = {'prd':'','vison':27017}
    DB_MDB_NAME = 'mdb_das'
    DB_MDB_USER = {'dev': 'dasdbuser', 'stg': '', 'prd': 'dasdbuser'}
    DB_MDB_PWD = {'dev': 'i7edi88nvufkls6wf', 'stg': '', 'prd': 'i7edi88nvufkls6wf'}

    HLL_ENV = options.env

    # MULTI_PROC = options.multi

    def __init__(self):
        pass

    def getEnvConf(self, _dict):
        if isinstance(_dict, str):
            return _dict
        if _dict.has_key(self.HLL_ENV):
            return _dict[self.HLL_ENV]
        if _dict.has_key('dev'):
            return _dict['dev']
        else:
            return False



