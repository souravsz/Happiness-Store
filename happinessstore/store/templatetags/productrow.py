from django import template


register= template.Library()

@register.filter
def productrow(productlist,count):
    datalist=[]
    i=0
    for products in productlist:
        datalist.append(products)
        i+=1
        if i == 4:
            i=0
            yield datalist
            datalist=[]
    if datalist:
        yield datalist
            
            
        
    