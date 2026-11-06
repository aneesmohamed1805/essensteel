"""Generate the review site's HTML from shared templates."""
from html import escape
from pathlib import Path

root = Path(__file__).parent / 'public'
nav = [('Products','products'),('Applications','sectors'),('Manufacturing','technology'),('Quality','standards'),('Contact','contact')]
products = [
 ('PC Strand','pc','Prestressing strand for concrete structures such as bridges, rail infrastructure and buildings.','Infrastructure'),
 ('ACSR Steel Core Wire & Strand','acsr','Steel core wire and strand for aluminium conductor steel reinforced (ACSR) used in overhead power transmission. Essen supplies the steel core component.','Power Transmission'),
 ('Galvanised Steel Wire','galv','Zinc-coated steel wire for applications such as fencing, cable armouring and nail manufacture.','Fencing and industrial use'),
 ('Mattress Spring Wire','spring','Steel wire for manufacturers that form springs for mattress assemblies.','Bedding'),
 ('Duct Wire','duct','Steel wire used in duct, cable installation and construction applications.','Cable installation'),
 ('Specialist Wires','special','Wire for cable armouring, fencing, nail manufacture and agricultural applications.','Industrial and agricultural use'),
]
applications = [('Power Transmission','power','acsr'),('Infrastructure','infra','pc'),('Bedding','bedding','spring')]
stories = [
 ('Understanding PC Strand','pc-strand','pc','How prestressing strand is used in concrete construction.','Prestressing puts the concrete into compression. PC strand carries the tensile force that is transferred to the concrete according to the structural design. When ordering, confirm the required grade, nominal diameter, governing standard, packaging and documentation with your technical team.'),
 ('What to Check in a Mill Test Report','mill-test-report','mill','How to check the report against your order and delivered material.','Start by matching the report identifier and batch or coil reference against the delivered material. Compare the reported grade, dimensions and test results with the requirements in your purchase order and applicable standard. Ask the supplier to clarify any missing values or discrepancies before releasing the material for use.'),
]
def link(path,label,cls=''):
    return f'<a class="{cls}" href="{path}">{escape(label)}</a>'

def button(path,label):
    return link(path,label+' →','button')

def section(content,style=''):
    return f'<section class="wrap section {style}">{content}</section>'

def photo(name,alt='',cls=''):
    return f'<img class="{cls}" src="/assets/{name}.webp" alt="{escape(alt,quote=True)}" loading="lazy">'

def page(path,title,description,body):
    links = ''.join(link('/'+slug+'/',name) for name,slug in nav)
    logo = '<a href="/" aria-label="Essen Steel home"><img class="logo" src="/assets/logo.webp" alt="Essen Steel" width="1511" height="778"></a>'
    target = root / path / 'index.html' if path != '404.html' else root / path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(f'''<!doctype html>
<html lang="en-GB">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Essen Steel</title>
<meta name="description" content="{escape(description,quote=True)}">
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="/assets/site.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="wrap bar">{logo}<nav aria-label="Main">{links}</nav></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="bar">{logo}<nav aria-label="Footer">{links}</nav></div>
<div class="row"><span>© 2026 Essen Steel</span><nav aria-label="Company">
{link('/about/','About')}{link('/projects/','Projects')}{link('/privacy-policy/','Privacy')}{link('/cookies/','Cookies')}</nav></div></div></footer>
</body></html>''',encoding='utf-8')

def interior(path,title,desc,content):
    page(path,title,desc,f'<div class="intro"><div class="wrap"><h1>{escape(title)}</h1><p>{escape(desc)}</p></div></div>{section(content,"prose")}')

def cards():
    return '<div class="grid">'+''.join(f'<a class="card" href="/products/{key}/"><span>{escape(name)}<br><b aria-hidden="true">→</b></span>{photo(key)}</a>' for name,key,_,_ in products)+'</div>'

def tiles():
    return '<div class="grid">'+''.join(f'<a class="tile" href="/sectors/#{img}" style="background-image:linear-gradient(0deg,#000d,transparent 90%),url(/assets/{img}.webp)"><span>{name}</span></a>' for name,img,_ in applications)+'</div>'

def stories_grid():
    return '<div class="dual">'+''.join(f'<a class="story" href="/insights/{slug}/">{photo(img)}<div><h3>{title}</h3><p>{desc}</p></div></a>' for title,slug,img,desc,_ in stories)+'</div>'

def heading(label):
    return f'<h2 class="rule">{label}</h2>'

steps = [('Draw','Reduce wire to the required size.'),('Strand','Form wire into strand where specified.'),('Test','Check against agreed requirements.'),('Prepare','Finish and pack for supply.'),('Supply','Coordinate delivery.')]
process = '<ol class="steps">'+''.join(f'<li><strong>{name}</strong>{desc}</li>' for name,desc in steps)+'</ol>'
factory = '<div class="factory"><div class="factory-inner"><div class="wrap"><span class="eyebrow">Green Manufacturing</span><h2>Consistent Quality<br>at Scale</h2><p>Wire drawing, stranding and quality checks support the production of steel wire and strand for a range of applications.</p>'+button('/technology/','Our Manufacturing')+'</div></div></div>'
hero = '<section class="hero"><img class="outline" src="/assets/outline.png" alt=""><div class="wrap"><h1>Steel Wire. Steel Strand.</h1>'+button('/products/','Explore Products')+'</div></section>'
resources = '''<div class="dual"><div><span class="eyebrow">Technical Resources</span><h2 class="normal">Product Data and Documentation</h2><p>Request the specification and documentation for your application.</p><a class="textlink" href="/downloads/">View Technical Resources →</a></div>
<div><span class="eyebrow">Partnership</span><h2 class="normal">A Better Supply Partnership</h2><p>Discuss your specification, quantity and delivery requirements with Essen Steel.</p><a class="textlink" href="/partnership/">Work With Us →</a></div></div>'''
page('', 'Steel Wire & Strand Manufacturer in the UAE','Explore Essen Steel wire and strand products, applications and technical resources. Request a quote from the sales team.',hero+section(heading('Our Process')+process)+factory+section(heading('Our Products')+cards())+section(resources)+section(heading('Applications')+tiles())+section('<div class="row">'+heading('Insights')+link('/insights/','View all insights →','textlink')+'</div>'+stories_grid()))
page('products','Steel Wire and Strand Products','Explore steel wires, strands and specialist products for industrial and infrastructure applications.',section('<h1>Our Products</h1><p>Choose a product to explore its use and discuss the specification with Essen Steel.</p>'+cards()))
for name,key,desc,uses in products:
    query = {'pc':'infra','acsr':'power','spring':'bedding'}.get(key,'other')
    interior(f'products/{key}',name,desc,photo(key,'Illustrative product detail','detail-photo')+f'<h2>Applications</h2><p>{uses}</p>'+link('/sectors/#'+query,'View applications','textlink')+'<h2>Discuss your specification</h2><p>Share the application, required grade, dimensions, quantity and delivery destination with our sales team.</p>'+button('/contact/','Request a Quote')+' <p>'+link('/downloads/','Request product documentation','textlink')+'</p>')
app_content = ''.join(f'<section id="{img}"><h2>{name}</h2><p>{products[[p[1] for p in products].index(key)][2]}</p>{link("/products/"+key+"/","View product","textlink")}</section>' for name,img,key in applications)
app_content += '<section id="other"><h2>Fencing, Agriculture and Industry</h2><p>Review galvanised steel wire and specialist wires for fencing, agricultural and industrial uses.</p>'+link('/products/','Explore the catalogue','textlink')+'</section>'
interior('sectors','Industries and Applications','Find the wire or strand used in your application.',app_content)
interior('technology','Manufacturing and Technology','Steel wire and strand production in Kizad, Abu Dhabi.',photo('factory','Illustrative wire production line','detail-photo')+'<h2>Drawing and stranding</h2><p>Wire is drawn to the required size and formed into strand where specified. Finishing, testing and packaging depend on the product and the agreed order requirements.</p>'+link('/sustainability/','Responsible manufacturing','textlink')+'<p>'+link('/standards/','Quality and documentation','textlink')+'</p>')
interior('standards','Quality and Certifications','Discuss product requirements, inspection and documentation.', '<h2>Quality documentation</h2><p>Share the standard, grade, inspection requirements and document format for your order. Ask Essen Steel for the current certificate and scope where your project requires third-party evidence.</p>'+button('/downloads/','Technical Resources'))
interior('sustainability','Responsible Manufacturing','Discuss the manufacturing information your project requires.','<p>When your procurement process calls for energy or environmental information, specify the product, reporting period and documents you need so the sales team can route your request.</p>'+button('/contact/','Contact Essen Steel'))
interior('about','About Essen Steel','Steel wire and strand manufacturer in Abu Dhabi, United Arab Emirates.','<p>Essen Steel supplies wire and strand for construction, power transmission, bedding and other industrial applications from Kizad, Abu Dhabi.</p>'+button('/products/','Explore Products'))
interior('partnership','Partnership and Supply','Discuss your specification and delivery requirements with Essen Steel.','<p>Include the intended application, product specification, quantity, packaging needs, destination and required delivery date in your enquiry.</p>'+button('/contact/','Request a Quote'))
interior('downloads','Technical Resources','Request product data sheets and quality documentation.','<p>Tell us the wire or strand you need and the standard or grade your order specifies. The sales team can confirm the applicable data sheet and documents for your enquiry.</p>'+button('mailto:sales@essensteel.com?subject=Product%20documentation%20request','Request Documentation'))
interior('projects','Project Enquiries','Discuss wire and strand requirements for your project.','<p>Tell the sales team what you are building, the product and standard you require, and your delivery timetable.</p>'+button('/contact/','Discuss Your Project'))
interior('contact','Contact Essen Steel','Request a quote or discuss your specification.','<p>For quotations, include your product, application, specification, quantity and delivery destination.</p>'+button('mailto:sales@essensteel.com?subject=Essen%20Steel%20quote%20request','Email a Quote Request')+'<p><a href="mailto:sales@essensteel.com">sales@essensteel.com</a><br><a href="tel:+97125109000">+971 2 510 9000</a></p><p>KHIA4-18D, Kizad A, Al Taweelah, Abu Dhabi, UAE</p>')
page('insights','Insights','Practical guides to steel strand and technical documentation.',section('<h1>Insights</h1>'+stories_grid()))
for title,slug,img,desc,body in stories:
    interior('insights/'+slug,title,desc,photo(img,'Illustrative detail','detail-photo')+f'<p>{body}</p>'+button('/downloads/','Technical Resources'))
interior('privacy-policy','Privacy','Information for visitors to this review build.','<p>Quote and documentation links open your email app. If you choose to send an email, Essen Steel receives the information you include in it.</p>')
interior('cookies','Cookies','Information for visitors to this review build.','<p>This preview uses no first-party cookies or analytics scripts. Its stylesheet requests the Exo typeface from Google Fonts.</p>')
interior('404.html','Page unavailable','The address may have changed.',button('/','Return to Home'))
