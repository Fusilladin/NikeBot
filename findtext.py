import re
html = 'sourcecode.txt'
with open(html,'r',encoding='utf-8') as file:
    var = file.read()
    file.close()
    pass

sk = 'skuId":"'
pattern = re.compile('(?<=' + sk + ').{36}(?=","localizedSize":")')
matches = pattern.finditer(var)
skuId = []
size_and_stock = {
     "sku_id" : []
    ,"nik_size" : []
    ,"loc_size" : []
    ,"stk" : []
}

for match in matches:
    x = match.group()
    size_and_stock["sku_id"].append(x)

    pattern = re.compile('(?<="nikeSize":")\d{1,2}(?:\.\d)?(?=","skuId":"' + x +'")')
    shoesize = pattern.finditer(var)
    for shoes in shoesize:
        shoes = shoes.group()
        size_and_stock['nik_size'].append(shoes)

    pattern = re.compile('(?<="'+ x +'","localizedSize":")\d{2}(?:\.\d)?(?=")')
    locsize = pattern.finditer(var)
    for loc in locsize:
        loc = loc.group()
        size_and_stock['loc_size'].append(loc)

    pattern = re.compile('(?<="level":")\w{3,7}(?=","skuId":"' + x +'")')
    stk = pattern.finditer(var)
    for amt in stk:
        amt = amt.group()
        size_and_stock['stk'].append(amt)
        
print(size_and_stock)
print(size_and_stock['sku_id'])
print(size_and_stock['nik_size'])
print(size_and_stock['loc_size'])
print(size_and_stock['stk'])
    

