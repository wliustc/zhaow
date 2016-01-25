import httplib
import urlparse

def request(url, cookie=''):
    ret = urlparse.urlparse(url)    # Parse input URL
    if ret.scheme == 'http':
        conn = httplib.HTTPConnection(ret.netloc)
    elif ret.scheme == 'https':
        conn = httplib.HTTPSConnection(ret.netloc)

    url = ret.path
    if ret.query: url += '?' + ret.query
    if ret.fragment: url += '#' + ret.fragment
    if not url: url = '/'

    conn.request(method='GET', url=url , headers={'Cookie': cookie})
    return conn.getresponse()

if __name__ == '__main__':
    cookie_str = 'Cookie:TGC=TGT1F6EEA4A8EB575182450302FBDC880A039E10472; __wmv=1445421100.73; __wms=1452739932; _portoData=b0138506-0f01-45d0-b456-a9014a887d1a; _fp_t_=123,1452738133064; WC_SERVER=5; _device_session_id=p_5ac6ca4b-dbc2-429c-b3d2-57d73a0d9bdf; __utma=1.1537476432.1441856089.1447172798.1448432845.11; __utmz=1.1446779884.9.8.utmcsr=suning.com|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_cb12e33a15345914e449a2ed82a2a216=1449669725,1450140426; cityId=9017; districtId=10118; SN_CITY=10_010_1000000_9017_13_10118_1_1; totalProdQty=1; _saPageSaleInfo=2218489779%3A108357066_undefined%7C144592716171220021%7Cssds_search_pro_buy03-1_0_0_108357066_0%2C136833900_0070117469%7C144592723231520704%7C%2C134966526_0070082915%7C14447015167137426%7C%2C132661550_0000000000%7C144592727612785152%7C%2C129818580_0070072392%7C144604115066182409%7C%2C129003082_0070092316%7C144653619242892849%7C%2C105939226_0070069225%7C144671019680577997%7C%2C134154999_0000000000%7C144707869639480864%7C%2C128209285_0000000000%7C144714045035539330%7C%2C126645029_0000000000%7C144715592769196829%7C%2C126520531_0000000000%7C144716179408324765%7C%2C135382055_0070088884%7C144732081201994998%7C%2C123158819_0070065747%7C144910614600087970%7C%2C138875540_0070122749%7C144966968632481622%7C%2C132372065_0070080175%7C14496702472676873%7C%2C125186073_0000000000%7C144991222532277032%7C%2C127841043_0070085501%7C145032219981950308%7C%2C121433607_0000000000%7C145032247446396790%7C; WC_PERSISTENT=WssOykJNF%2blVbXsrapEsbgUMEvQ%3d%0a%3b2016%2d01%2d12+15%3a10%3a22%2e25%5f1452582622249%2d19187%5f10052; sesab=a; sesabv=36%2390%3A10; smhst=138095083a138095945a124168486a131777313a128991565a131331917a131331915a131331908a104231716a132993774a106082745a133618135a121433607a138891075a103636621a135342549a127841043a135151296a125764268a133832407; _snsr=direct%7Cdirect%7C%7C%7C; cart_abtest_num=53; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=%2d1002%2cjnefR7OrhqcfkBcZd%2bCp0iOYFhA%3d; WC_ACTIVEPOINTER=%2d7%2c10052; WC_USERACTIVITY_-1002=%2d1002%2c10052%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cHfu4AyHVyTEH5%2fLoLwRp0%2frI3cWrBquyD%2fSaNhM3UZ0lBXgogKjO%2fnlhmMBqRneXE2OgTee1sa27%0aQuwpNH4ryhE1MVIGWXkdKD%2fHP%2fjWX%2fdF1FemvjVQmhNNUMrVA0reOvOft3S1j2to3F1bys9vEA%3d%3d; WC_GENERIC_ACTIVITYDATA=[50000151097128866%3atrue%3afalse%3a0%3aNtDjuN7bvj370UkxPNCAnJsgr4c%3d][com.ibm.commerce.context.audit.AuditContext|1452582622249%2d19187][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|%2d7%26CNY%26%2d7%26CNY][com.ibm.commerce.catalog.businesscontext.CatalogContext|null%26null%26false%26false%26false][com.suning.commerce.context.common.SNContext|9173%26%2d1%26null%26172%2e19%2e136%2e86%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null%26null][com.ibm.commerce.context.base.BaseContext|10052%26%2d1002%26%2d1002%26%2d1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10007%2610007%26null%26%2d2000%26null%26null%26null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; __wmv=1445421100.72; cart_abtest=B; _ga=GA1.2.1537476432.1441856089; _gat=1; custno=2218489779; idsLoginUserIdLastTime=zw19881%40163.com; logonStatus=2; nick=zhaow_123...; _snma=1%7C144185608861781903%7C1441856088617%7C1452738132748%7C1452738144172%7C1971%7C193; _snmc=1; authId=si3D02E4568F3A9266CB2F1103ECF1D395; nick2=zhaow_123...; secureToken=39F6EF215C516ED3A1224023319EE46F; _snmp=145273814352722640; _snmb=145273596840245935%7C1452738144577%7C1452738144177%7C10'
    url = 'http://try.suning.com/tps/apply/go1000017842_1.htm'
    html_doc = request(url, cookie_str).read()
    print 'html_doc %s' %html_doc
    import re
    print 'With Auth:', re.search('<title>(.*?)</title>', html_doc, re.IGNORECASE).group(1)

    html_doc = request(url).read()
    print 'Without Auth:', re.search('<title>(.*?)</title>', html_doc, re.IGNORECASE).group(1)