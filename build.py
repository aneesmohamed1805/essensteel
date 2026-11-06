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

pantheon_media = 'https://dev-essen-steel-2.pantheonsite.io/wp-content/uploads/2026/03/'
interior_visuals = {
    'about': ('factory', ''),
    'technology': ('factory', 'essen-manufacturing.webp'),
    'standards': ('mill', ''),
    'sustainability': ('factory', ''),
    'sectors': ('infra', 'essen-products-banner.webp'),
}

def visual_style(fallback, source=''):
    layers = [f'url(/assets/{fallback}.webp)']
    if source:
        layers.insert(0, f'url({pantheon_media}{source})')
    return ','.join(layers)

def interior(path,title,desc,content):
    visual = interior_visuals.get(path)
    if path.startswith('products/'):
        visual = (path.split('/')[1], '')
    intro_class = 'intro'
    art = ''
    if visual:
        intro_class += ' intro-visual'
        art = f'<div class="intro-art" style="background-image:{visual_style(*visual)}" aria-hidden="true"></div>'
    body_class = '' if path == 'sectors' else 'prose'
    page(path,title,desc,f'<div class="{intro_class}">{art}<div class="wrap"><h1>{escape(title)}</h1><p>{escape(desc)}</p></div></div>{section(content,body_class)}')

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
catalogue = """<h1>Our Products</h1>
<p>Essen Steel manufactures steel wire and strand in Abu Dhabi for infrastructure, construction, power transmission, agriculture and industrial manufacturing. Use the catalogue to identify the product family, then discuss the grade, dimensions and documentation your order requires.</p>"""
page('products','Steel Wire and Strand Products','Explore steel wires, strands and specialist products for industrial and infrastructure applications.',section(catalogue+cards())+section("""
<h2>Steel wire products</h2>
<p>Galvanised steel wire is used in fencing, cable armouring and nail manufacture. Mattress spring wire is formed into springs for bedding, while duct wire serves cable installation and construction applications.</p>
<h2>Steel strands</h2>
<p>Prestressed concrete strand is used in bridges, rail infrastructure and buildings. ACSR steel core wire and strand reinforce aluminium conductors used in overhead power transmission. Confirm the required construction and grade against the applicable data sheet.</p>
<h2>Specialist wires</h2>
<p>For cable armouring, fence, nail or agricultural wire, share the intended application and the processing or installation requirements with Essen Steel.</p>
"""+button('/contact/','Discuss Your Specification'),'prose'))
product_notes = {
    'pc': 'For prestressing orders, share the governing standard, strand designation, nominal diameter and required test documentation. Confirm the coil or pack requirements with your installation team.',
    'acsr': 'Give the conductor designation, core construction, wire diameter and applicable coating requirement. The complete conductor specification helps identify the steel core needed.',
    'galv': 'Share the wire diameter, required tensile properties, coating specification and intended application. Include the pack or coil format needed for your downstream process.',
    'spring': 'Share the wire diameter, spring design requirements and the pack format your forming equipment uses. Confirm the mechanical properties required for your application.',
    'duct': 'Describe how the wire is used in your duct or cable installation and identify the dimensional and handling requirements for the order.',
    'special': 'Identify the end use, such as cable armouring, fencing, nail manufacture or agriculture. Share any forming, coating or packaging requirements that affect downstream processing.',
}
for name,key,desc,uses in products:
    query = {'pc':'infra','acsr':'power','spring':'bedding'}.get(key,'other')
    interior(f'products/{key}',name,desc,f'<h2>Applications</h2><p>{uses}</p>'+link('/sectors/#'+query,'View applications','textlink')+f'<h2>Discuss your specification</h2><p>{product_notes[key]}</p><p>Include your quantity, delivery destination and target date when requesting a quote.</p>'+button('/contact/','Request a Quote')+' <p>'+link('/downloads/','Request product documentation','textlink')+'</p>')
sector_details = [
    ('infra','Infrastructure','infra','essen-infrastructure.webp','Prestressing strand is used in concrete bridges, rail infrastructure and other civil works. Share the governing standard, strand designation and test documentation required by the structural design.','pc','PC Strand'),
    ('construction','Construction','infra','essen-construction-b.webp','Prestressed concrete elements are used in buildings and other structures. Confirm the specified strand, nominal diameter, packaging and handling requirements with the project team.','pc','PC Strand'),
    ('power','Power Transmission','power','','Steel core wire and strand reinforce the aluminium wires in ACSR overhead conductors. Include the conductor designation and the steel core construction in your enquiry.','acsr','ACSR Steel Core Wire and Strand'),
    ('telecommunications','Telecommunications','duct','essen-telecommunication.webp','Duct wire is used in cable installation. Steel wire may also be specified for cable armouring. Share how the wire will be used, along with dimensions, coating requirements and the governing specification.','duct','Duct Wire'),
    ('other','Agriculture and Fencing','galv','essen-fencing.webp','Galvanised steel wire is used for agricultural and fencing applications. Include the wire diameter, coating requirements and intended installation or downstream process.','galv','Galvanised Steel Wire'),
    ('manufacturing','Manufacturing','factory','essen-manufacturing.webp','Industrial buyers use steel wire for applications such as nail manufacture, cable armouring and other downstream processing. Share the forming process and the mechanical and packaging requirements.','special','Specialist Wires'),
    ('bedding','Bedding','bedding','','Mattress manufacturers form spring wire into components for bedding assemblies. Tell us the wire diameter, required mechanical properties and pack format for your forming equipment.','spring','Mattress Spring Wire'),
]
sector_nav = '<nav class="sector-nav" aria-label="Jump to sector">'+''.join(link('#'+key,title) for key,title,*_ in sector_details)+'</nav>'
sector_panels = []
for key,title,fallback,source,body,product,label in sector_details:
    art = f'<div class="sector-art" style="background-image:{visual_style(fallback,source)}" aria-hidden="true"></div>'
    copy = f'<div class="sector-copy"><h2>{title}</h2><p>{body}</p>{link("/products/"+product+"/",label+" →","textlink")}</div>'
    sector_panels.append(f'<section class="sector-panel" id="{key}">{art}{copy}</section>')
app_content = sector_nav+'<div class="sector-panels">'+''.join(sector_panels)+'</div>'
interior('sectors','Industries and Applications','Explore how Essen Steel wire and strand are used across infrastructure, construction, power, telecommunications, agriculture, fencing and manufacturing.',app_content)
interior('technology','Manufacturing and Technology','Steel wire and strand production in Kizad, Abu Dhabi.',"""
<section><h2>Wire drawing and stranding</h2><p>Wire drawing reduces the material to the diameter required for the order. Where the product is a strand, individual wires are formed into the specified construction. The required dimensions and mechanical properties depend on the product and its application.</p></section>
<section><h2>Finishing and galvanising</h2><p>Finishing depends on the intended use. For galvanised products, the coating specification forms part of the order alongside the wire dimensions and mechanical requirements.</p></section>
<section><h2>Testing and traceability</h2><p>Inspection and testing connect the manufacturing process to the buyer’s specification. Agree the relevant dimensional, mechanical and coating checks, along with any test reports and material identification required for delivery.</p></section>
<section><h2>Packaging and supply</h2><p>Share how the material will be handled and processed at the destination. Agree the packaging, labelling, quantity and delivery requirements as part of the order.</p></section>
"""+link('/sustainability/','Responsible manufacturing','textlink')+'<p>'+link('/standards/','Quality and documentation','textlink')+'</p>')
interior('standards','Quality and Certifications','Discuss product requirements, inspection and documentation.',"""
<section><h2>Quality assurance through production</h2><p>Quality assurance covers incoming material inspection, checks during production and final verification against the specification. Agree any project-specific inspection or acceptance requirements when requesting a quote.</p></section>
<section><h2>Mechanical, dimensional and coating checks</h2><p>Relevant checks may include tensile strength, elongation and dimensions. For galvanised products, specify the coating requirement and the test method or reporting format your project needs.</p></section>
<section><h2>Material traceability</h2><p>When mill test reports are required, agree the batch or coil identification and the information to appear in the report. Match the material identification and report to the purchase specification at receipt.</p></section>
<section><h2>Certification and approval documents</h2><p>Ask for the current certificate and scope for the product or facility involved. Identify whether the project requires management-system certification, product certification or an authority approval.</p></section>
""".replace('Quality assurance covers','Quality assurance covers')+button('/downloads/','Technical Resources'))
interior('sustainability','Responsible Manufacturing','Manufacturing practices and environmental information for procurement teams.',"""
<section><h2>Energy and resource use</h2><p>Energy use, material waste and process control are focus areas for responsible wire and strand manufacturing. Buyers who track these factors can specify the product, reporting boundary and period they need when requesting evidence.</p></section>
<section><h2>Material selection and service conditions</h2><p>The right grade, dimensions and coating depend on the application. Share the operating conditions and applicable standard so the material specification can be reviewed for the intended use.</p></section>
<section><h2>Environmental documentation</h2><p>For supplier assessments or tenders, include the exact environmental or energy documentation required and any applicable reporting format.</p></section>
"""+button('/contact/','Request Manufacturing Information'))
interior('about','About Essen Steel','Steel wire and strand manufacturer in Abu Dhabi, United Arab Emirates.',"""
<section><h2>What Essen manufactures</h2><p>From its facility in Kizad, Abu Dhabi, Essen Steel manufactures steel wire and strand for infrastructure, power transmission, construction and industrial manufacturing. The range includes prestressed concrete strand, ACSR steel core wire and strand, galvanised wire and specialist wires.</p></section>
<section><h2>What the products support</h2><p>Prestressing strand is used in concrete structures such as bridges, rail infrastructure and buildings. Steel core wire and strand are used in ACSR conductors, while other wire products serve bedding, fencing, agriculture and cable applications.</p></section>
<section><h2>How Essen works with buyers</h2><p>Essen works with engineers, procurement teams and manufacturers to clarify material requirements before supply. The discussion can cover the applicable standard, product grade, quantity, test documentation, packaging and delivery destination.</p></section>
<section><h2>Supply from the UAE</h2><p>For UAE or international enquiries, provide the delivery location and required timeframe so the sales team can review the order and discuss available arrangements.</p></section>
"""+button('/products/','Explore Products'))
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
