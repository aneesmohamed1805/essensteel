"""Generate the review site's HTML from shared templates."""
from html import escape
import json
import re
from pathlib import Path

root = Path(__file__).parent / 'public'
nav = [('Products','products'),('Applications','sectors'),('Manufacturing','technology'),('Insights','insights'),('Contact','contact')]
products = [
 ('PC Strand','pc','Prestressing strand for concrete structures such as bridges, rail infrastructure and buildings.','Infrastructure'),
 ('ACSR Steel Core Wire & Strand','acsr','Steel core wire and strand for aluminium conductor steel reinforced (ACSR) used in overhead power transmission. Essen supplies the steel core component.','Power Transmission'),
 ('Galvanised Steel Wire','galv','Zinc-coated steel wire for applications such as fencing, cable armouring and nail manufacture.','Fencing and industrial use'),
 ('Mattress Spring Wire','spring','Steel wire for manufacturers that form springs for mattress assemblies.','Bedding'),
 ('Duct Wire','duct','Steel wire used in duct, cable installation and construction applications.','Cable installation'),
 ('Specialist Wires','special','Wire for cable armouring, fencing, nail manufacture and agricultural applications.','Industrial and agricultural use'),
]
applications = [('Power Transmission','power','acsr'),('Infrastructure','infra','pc'),('Bedding','bedding','spring')]
# Add new articles at the top. The homepage displays the first two.
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

visual_assets = {
    'pc': 'catalogue-editorial', 'acsr': 'power', 'spring': 'bedding',
    'hero': 'catalogue-editorial', 'factory': 'industrial-hall',
}
def photo(name,alt='',cls=''):
    name = visual_assets.get(name, name)
    return f'<img class="{cls}" src="/assets/{name}.webp" alt="{escape(alt,quote=True)}" loading="lazy">'

# Keep the approved page templates intact while assigning one image to each slot.
image_placements = json.loads(Path(__file__).with_name('image-placements.json').read_text())
image_reference = re.compile(r'/assets/[\w-]+\.webp(?:" alt="[^"]*")?')

def place_images(path, body):
    if path.startswith('insights/') and path not in image_placements:
        return body
    planned = image_placements.get(path, [])
    actual = list(image_reference.finditer(body))
    if len(actual) != len(planned):
        raise ValueError(f'{path or "homepage"} has {len(actual)} image slots, expected {len(planned)}')
    for match, asset in reversed(list(zip(actual, planned))):
        name, _, alt = asset.partition('|')
        previous = match.group()
        suffix = previous[previous.index('" alt='):] if '" alt=' in previous else ''
        if alt and suffix:
            suffix = f'" alt="{escape(alt,quote=True)}"'
        body = body[:match.start()] + f'/assets/{name}.webp{suffix}' + body[match.end():]
    return body

def page(path,title,description,body):
    body = place_images(path, body)
    links = ''.join(link('/'+slug+'/',name) for name,slug in nav)
    submenus = {
        'corporate': [('/about/', 'About'), ('/partnership/', 'Partnership & Supply')],
        'technology': [('/technology/', 'Overview'), ('/technology/#green-manufacturing', 'Green Manufacturing'), ('/standards/', 'Quality'), ('/downloads/', 'Technical Resources')],
    }
    main_links = []
    for name, slug in [('Corporate', 'corporate'), *nav]:
        parent = link('/'+slug+'/', name)
        if slug in submenus:
            children = ''.join(f'<li>{link(path, label)}</li>' for path, label in submenus[slug])
            parent = f'<details class="subnav corporate-nav"><summary>{name}<span aria-hidden="true"></span></summary><ul>{children}</ul></details>'
        main_links.append(parent)
    main_menu = ''.join(main_links)
    footer_links = link('/about/','About') + links
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
<header class="wrap bar">{logo}<nav aria-label="Main">{main_menu}</nav></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="bar">{logo}<nav aria-label="Footer">{footer_links}</nav></div>
<div class="row"><span>© 2026 Essen Steel</span><nav aria-label="Company">
{link('/projects/','Projects')}{link('/privacy-policy/','Privacy')}{link('/cookies/','Cookies')}</nav></div></div></footer>
</body></html>''',encoding='utf-8')

interior_visuals = {
    'about': 'about-editorial', 'technology': 'factory', 'standards': 'hero',
    'sustainability': 'factory', 'sectors': 'infra', 'insights': 'catalogue-editorial',
    'contact': 'contact-editorial', 'products': 'catalogue-editorial', 'partnership': 'hero', 'downloads': 'hero', 'projects': 'infra',
}

def visual_style(asset):
    return f'url(/assets/{visual_assets.get(asset, asset)}.webp)'

def feature(heading, paragraphs, asset, alt, path, label):
    copy = ''.join(f'<p>{escape(paragraph)}</p>' for paragraph in paragraphs)
    return f'<section class="sector-panel feature-panel">{photo(asset, alt, "feature-art")}<div class="sector-copy"><h2>{escape(heading)}</h2>{copy}{link(path,label+" →","textlink")}</div></section>'

def feature_group(*features):
    return '<div class="sector-panels">'+''.join(features)+'</div>'

def interior(path,title,desc,content):
    visual = interior_visuals.get(path)
    if path.startswith('products/'):
        visual = 'catalogue-editorial'
    intro_class = 'intro'
    art = ''
    if visual:
        intro_class += ' intro-visual'
        art = f'<div class="intro-art" style="background-image:{visual_style(visual)}" aria-hidden="true"></div>'
    body_class = '' if path in ('products','contact','insights') or 'sector-panels' in content else 'prose'
    page(path,title,desc,f'<div class="{intro_class}">{art}<div class="wrap"><h1>{escape(title)}</h1><p>{escape(desc)}</p></div></div>{section(content,body_class)}')

def cards():
    return '<div class="grid">'+''.join(f'<a class="card" href="/products/{key}/"><span>{escape(name)}<br><b aria-hidden="true">→</b></span>{photo(key)}</a>' for name,key,_,_ in products)+'</div>'

def tiles():
    return '<div class="grid">'+''.join(f'<a class="tile" href="/sectors/#{img}" style="background-image:linear-gradient(0deg,#000d,transparent 90%),url(/assets/{img}.webp)"><span>{name}</span></a>' for name,img,_ in applications)+'</div>'

def stories_grid(*, homepage=False):
    selected = stories[:2] if homepage else stories
    prefix = 'home' if homepage else 'index'
    cards = []
    for title, slug, _, desc, _ in selected:
        src = f'/assets/insights/{prefix}-{slug}.webp'
        if not (root / src.lstrip('/')).is_file():
            raise FileNotFoundError(src)
        cards.append(f'<a class="story" href="/insights/{slug}/"><img src="{src}" alt="" loading="lazy"><div><h3>{escape(title)}</h3><p>{escape(desc)}</p></div></a>')
    return '<div class="dual">' + ''.join(cards) + '</div>' 

def heading(label):
    return f'<h2 class="rule">{label}</h2>'

steps = [('Draw','Reduce wire to the required size.'),('Strand','Form wire into strand where specified.'),('Test','Check against agreed requirements.'),('Prepare','Finish and pack for supply.'),('Supply','Coordinate delivery.')]
process = '<ol class="steps">'+''.join(f'<li><strong>{name}</strong>{desc}</li>' for name,desc in steps)+'</ol>'
factory = '<div class="factory"><div class="factory-inner"><div class="wrap"><span class="eyebrow">Green Manufacturing</span><h2>Resource Efficiency<br>in Wire Production</h2><p>Wire drawing, stranding and quality checks support the production of steel wire and strand for a range of applications.</p>'+button('/technology/','Our Manufacturing')+'</div></div></div>'
hero = '<section class="hero"><img class="outline" src="/assets/outline.png" alt=""><div class="wrap"><h1>Steel Wire. Steel Strand.</h1><p>Made in Abu Dhabi for concrete infrastructure, overhead power networks and industrial production.</p>'+button('/products/','Explore Products')+'<small class="hero-caption">Illustrative infrastructure project</small></div></section>'
resources = '''<div class="dual"><div><span class="eyebrow">Technical Resources</span><h2 class="normal">Product Data and Documentation</h2><p>Request the specification and documentation for your application.</p><a class="textlink" href="/downloads/">View Technical Resources →</a></div>
<div><span class="eyebrow">Partnership</span><h2 class="normal">A Better Supply Partnership</h2><p>Discuss your specification, quantity and delivery requirements with Essen Steel.</p><a class="textlink" href="/partnership/">Work With Us →</a></div></div>'''
page('', 'Steel Wire & Strand Manufacturer in the UAE','Explore Essen Steel wire and strand products, applications and technical resources. Request a quote from the sales team.',hero+section(heading('Our Process')+process)+factory+section(heading('Our Products')+cards())+section(resources)+section(heading('Applications')+tiles())+section('<div class="row">'+heading('Insights')+link('/insights/','View all insights →','textlink')+'</div>'+stories_grid(homepage=True)))
product_context = {
    'pc': ('Concrete infrastructure', 'infra'),
    'acsr': ('Overhead power transmission', 'power'),
    'galv': ('Fencing and industrial use', 'galv'),
    'spring': ('Mattress and bedding production', 'bedding'),
    'duct': ('Duct and cable installation', 'duct'),
    'special': ('Downstream wire processing', 'special'),
}
catalogue_cards = []
for name,key,description,_ in products:
    application,asset = product_context[key]
    catalogue_cards.append(f"""
    <article class="catalogue-card">
      <a class="catalogue-visual" href="/products/{key}/" aria-label="{escape(name,quote=True)}">
        {photo(asset, '', 'catalogue-image')}
        <span class="catalogue-index">{escape(application)}</span>
      </a>
      <div class="catalogue-copy">
        <h3>{link('/products/'+key+'/',name)}</h3>
        <p>{escape(description)}</p>
        {link('/products/'+key+'/','Product details →','textlink')}
      </div>
    </article>""")
catalogue = """
<div class="section-lead"><span class="eyebrow">The product range</span><h2 class="rule">Find the wire or strand for your application</h2>
<p>Choose a product family to see what Essen supplies and the information to share with your enquiry. For project-specific grades, dimensions or certification, request the applicable documentation.</p></div>
<div class="catalogue-grid">"""+''.join(catalogue_cards)+"""</div>
<div class="catalogue-guide"><div><span class="eyebrow">From application to specification</span><h2>Know what the material needs to do?</h2><p>Explore the industries Essen serves to identify the relevant wire or strand.</p><a class="textlink" href="/sectors/">Browse applications →</a></div>
<div><span class="eyebrow">From specification to enquiry</span><h2>Already have a material specification?</h2><p>Share the grade, standard, dimensions, quantity and delivery destination with the sales team.</p><a class="textlink" href="/contact/#quote">Request a quote →</a></div></div>
"""
interior('products','Steel Wire and Strand Products','Explore Essen Steel’s six product families for construction, power transmission and industrial manufacturing.',catalogue)
product_notes = {
    'pc': 'For prestressing orders, share the governing standard, strand designation, nominal diameter and required test documentation. Confirm the coil or pack requirements with your installation team.',
    'acsr': 'Give the conductor designation, core construction, wire diameter and applicable coating requirement. The complete conductor specification helps identify the steel core needed.',
    'galv': 'Share the wire diameter, required tensile properties, coating specification and intended application. Include the pack or coil format needed for your downstream process.',
    'spring': 'Share the wire diameter, spring design requirements and the pack format your forming equipment uses. Confirm the mechanical properties required for your application.',
    'duct': 'Describe how the wire is used in your duct or cable installation and identify the dimensional and handling requirements for the order.',
    'special': 'Identify the end use, such as cable armouring, fencing, nail manufacture or agriculture. Share any forming, coating or packaging requirements that affect downstream processing.',
}
application_examples = {
    'pc': 'In a concrete viaduct, the strand is tensioned to introduce compression into the girders that span between piers.',
    'acsr': 'Between transmission towers, the steel core reinforces the aluminium wires that carry the current.',
    'galv': 'For outdoor fencing, a zinc coating helps protect the wire from corrosion while the mesh defines the enclosure.',
    'spring': 'A spring-forming line turns straight wire into the coils that make up the mattress support unit.',
    'duct': 'A duct installation is one stage of a cable route. Specify the wire by its role in that installation.',
    'special': 'In downstream forming, feed and guide requirements are part of selecting a wire for the finished component.',
}
for name,key,desc,uses in products:
    query = {'pc':'infra','acsr':'power','spring':'bedding'}.get(key,'other')
    interior(f'products/{key}',name,desc,feature_group(feature('Where it is used', [desc, application_examples[key]], product_context[key][1], 'Illustrative '+uses.lower()+' application', '/sectors/#'+query, 'View applications'), feature('What to specify', [product_notes[key], 'Include your quantity, delivery destination and target date when requesting a quote. Identify any certificate, inspection requirement or material test report that forms part of the order.'], key, 'Illustrative material or application detail', '/downloads/', 'Request product documentation'))+button('/contact/','Request a Quote')+' <p>'+link('/downloads/','Request product documentation','textlink')+'</p>')
sector_details = [
    ('infra','Infrastructure','infra','In a concrete viaduct, prestressing strand helps the girders carry loads between piers. Tension in the strand puts the concrete into compression. The structural design governs the strand designation, dimensions and test requirements.','pc','PC Strand'),
    ('construction','Construction','construction','Precast beams and floor units can be prestressed before they leave the casting yard. In pre-tensioned production, strand is tensioned in the casting bed and transfers that force to the concrete after it has gained sufficient strength.','pc','PC Strand'),
    ('power','Power Transmission','power','An overhead line conductor has to span the distance between towers while carrying electrical current. In ACSR construction, the aluminium wires carry the current and the steel core provides reinforcement. Essen supplies the steel core wire or strand.','acsr','ACSR Steel Core Wire and Strand'),
    ('telecommunications','Telecommunications','duct','A telecom duct route and the cable installed within it are separate parts of the system. Duct wire is used in cable installation, while armouring wire may form part of the cable itself. Identify which application your specification covers.','duct','Duct Wire'),
    ('other','Agriculture and Fencing','galv','Wire for outdoor fencing is formed into mesh or used in other fence components. The zinc coating helps protect the steel against corrosion. For agriculture and fencing orders, confirm the intended exposure, wire diameter and coating requirement.','galv','Galvanised Steel Wire'),
    ('manufacturing','Manufacturing','special','On a forming line, guides and rollers feed steel wire into the next operation. The finished part may be a nail, a cable armouring component or another industrial product. The forming process determines what the wire needs to do.','special','Specialist Wires'),
    ('bedding','Bedding','bedding','The individual coils in a mattress spring unit start as steel spring wire. Bedding manufacturers form that wire into coils, then assemble them into the support system specified for the mattress.','spring','Mattress Spring Wire'),
]
sector_nav = '<nav class="sector-nav" aria-label="Jump to sector">'+''.join(link('#'+key,title) for key,title,*_ in sector_details)+'</nav>'
sector_context = {
    'infra': 'For staged civil works, include the quantity and delivery window for each stage. Identify any inspection and material traceability requirements before placing the order.',
    'construction': 'The project team should specify strand for the intended system, whether precast, post-tensioned or another designed application. Include any restrictions on pack dimensions, handling or storage at the plant or site.',
    'power': 'Conductor manufacturers should identify the required core diameter, coating and mechanical properties. For aluminium-clad steel or overhead ground wire enquiries, give the designation and construction so the sales team can confirm availability and documentation.',
    'telecommunications': 'Identify whether the wire is for a duct installation or an armouring process. The intended function determines the specification and which wire family to discuss.',
    'other': 'Applications include chain-link and welded mesh, gabion baskets, poultry mesh, crop trellises and vineyard support. Confirm the wire specification with the fabricator and share the intended exposure, forming process and pack format.',
    'manufacturing': 'Engineering uses also include binding wire for tying reinforcement. Share how the wire is fed, formed or cut and which dimensions and mechanical properties affect the process. Note any limits on coil size or pack weight.',
    'bedding': 'Include the spring design requirements and how the wire feeds into your forming equipment. Confirm the pack format and the properties your production team needs to check.',
}
sector_image_descriptions = {
    'infra': 'Illustrative concrete viaduct crossing a rocky valley',
    'construction': 'Illustrative precast concrete beams stored in a casting yard',
    'power': 'Illustrative overhead transmission towers and suspended conductors',
    'telecommunications': 'Illustrative telecom conduits and cable installation site',
    'other': 'Illustrative galvanised wire fencing and a wire roll',
    'manufacturing': 'Illustrative steel wire feeding through a forming line',
    'bedding': 'Illustrative mattress spring coils on a production bench',
}
sector_panels = []
for key,title,asset,body,product,label in sector_details:
    art = photo(asset, sector_image_descriptions[key], "sector-art")
    copy = f'<div class="sector-copy"><h2>{title}</h2><p>{body}</p><p>{sector_context[key]}</p>{link("/products/"+product+"/",label+" →","textlink")}</div>'
    sector_panels.append(f'<section class="sector-panel" id="{key}">{art}{copy}</section>')
app_content = sector_nav+'<div class="sector-panels">'+''.join(sector_panels)+'</div>'
interior('sectors','Industries and Applications','Explore how Essen Steel wire and strand are used across infrastructure, construction, power, telecommunications, agriculture, fencing and manufacturing.',app_content)
green_manufacturing = f"""
<section class="green-manufacturing" id="green-manufacturing">
  {photo('green-overview', 'Illustrative steel wire offcuts collected beside wire coils')}
  <div class="green-manufacturing-copy">
  <h2 class="rule">Green Manufacturing</h2>
  <p>Essen Steel’s technology information identifies Galva Green as a galvanising process used for steel wire. Energy use, material yield and the handling of steel offcuts are useful areas to review when assessing the production route for a particular product.</p>
  <p>For a supplier assessment or tender, specify the product or facility, the reporting period and the evidence you need. Facility energy figures and product-level environmental information answer different questions.</p>
  <a class="textlink" href="/sustainability/">Explore responsible manufacturing →</a>
  </div>
</section>"""
interior('technology','Manufacturing and Technology','From drawn wire to finished strand, see how the specification carries through production and supply.',feature_group(
    feature('Drawing and stranding', [
        'Drawing reduces steel wire to the diameter required for its next operation. For a strand, individual wires are formed into the required construction. Prestressing strand and ACSR steel core strand serve different applications and need their own order specifications.',
        'Start with the product designation and governing standard. Those details help establish which dimensions, mechanical properties and construction need to be checked.'
    ], 'industrial-hall','Illustrative wire-drawing line','/products/','Explore the product range'),
    feature('A zinc coating for exposed wire', [
        'The zinc coating on galvanised wire helps protect the steel surface in applications such as outdoor fencing. The order must describe the coating as well as the wire beneath it. Mesh forming and cable armouring can call for different combinations of dimensions, coating and mechanical properties.',
        'If the wire runs through forming or feeding equipment, tell us how it is handled and what coil or pack arrangement that equipment accepts.'
    ],'galv','Illustrative galvanised steel wire','/products/galv/','Explore galvanised wire'),
    feature('Inspection, packing and dispatch', [
        'A labelled coil and its inspection record give the receiving team two points to match before material enters production. Agree the identifiers, report format and checks required for the order before packing and dispatch.',
        'Confirm the pack configuration, quantity, destination and delivery window before ordering. Let us know about unloading restrictions or staging requirements.'
    ],'mill','Illustrative coil tag and inspection worksheet','/standards/','Review quality and documentation'),
    feature('Inline treatment and specialist lines', [
        'Essen Steel’s technology information describes inline E-Phos treatment for phosphate-coated wire. This is a surface treatment step within the wire drawing line. The required finish depends on the product and the buyer’s downstream process.',
        'The technology range also includes low-relaxation strand production, aluminium cladding and stranding. For low-relaxation PC strand, share the project’s grade and test requirements. For aluminium-clad steel, specify the wire or strand construction and the applicable standard.'
    ],'audit-technology','Illustrative inline wire treatment and guide rollers','/downloads/','Request process and product information')
)+green_manufacturing)
interior('standards','Quality and Certifications','What engineers and procurement teams should agree before ordering and check when receiving material.',feature_group(
    feature('Agree the acceptance criteria', [
        'Coiled wire and finished strand can look similar at a glance while serving very different functions. The purchase specification identifies the product, grade and dimensions and sets the acceptance criteria for that material.',
        'Depending on the product, the specification may call for tensile or elongation results, dimensional tolerances or coating checks. Ask which results will appear on the order documentation.'
    ],'pc','Illustrative steel strand detail','/downloads/','Request technical documentation'),
    feature('Match the coil tag to the test report', [
        'Start with the identifier on the coil tag. Match it to the batch or coil reference on the mill test report, then compare the documented grade, dimensions and test results with the purchase specification.',
        'If the identifiers or values differ, raise the discrepancy with the supplier before releasing the material for use.'
    ],'mill','Illustrative coil tag and inspection worksheet','/insights/mill-test-report/','Read the mill test report guide'),
    feature('Check certificates for scope', [
        'A management-system certificate covers a defined system and facility. A product certificate covers specified products, and an authority approval has its own scope. Ask for the document applicable to your product, facility and project.',
        'Review the issuing body, covered scope and validity against your tender or procurement requirements.'
    ],'factory','Illustrative manufacturing equipment','/contact/','Request the applicable documents'),
    feature('In-house material testing', [
        'Essen Steel’s standards information describes checks that begin with incoming wire rod and continue through product verification. The laboratory uses universal testing equipment and extensometers to measure mechanical properties, including extension under load.',
        'If your specification requires a particular test, identify the method, sampling requirements and reporting format when you place the enquiry.'
    ],'audit-testing','Illustrative steel wire specimen in a universal testing machine','/downloads/','Request testing documentation')
))
interior('sustainability','Responsible Manufacturing','What to ask about resource use, material selection and evidence for your procurement process.',feature_group(
    feature('Define what you need to measure', [
        'Energy use and material waste are relevant to wire and strand manufacturing. If your supplier assessment asks for these figures, identify the product or facility, the reporting period and the boundary you need covered.',
        'Specify whether you need a facility-level figure or product-level documentation. The two answer different questions and should be compared on a consistent basis.'
    ],'factory','Illustrative production line','/contact/','Request manufacturing information'),
    feature('Specify for the intended service', [
        'Material choice starts with the application and its service conditions. For wire used outdoors or in other exposure conditions, share the governing standard, required coating and intended use with the technical team.',
        'For tenders, include the documentation format and any reporting or verification requirements with the enquiry.'
    ],'galv','Illustrative zinc-coated wire','/products/galv/','Explore galvanised wire')
))
interior('about','About Essen Steel','A UAE manufacturer of steel wire and strand, based in Kizad, Abu Dhabi.',feature_group(
    feature('Wire and strand from Abu Dhabi', [
        'Essen Steel manufactures steel wire and strand for buyers who need to match a material to a specific design, process or installation. Its range includes prestressed concrete strand, ACSR steel core wire and strand, galvanised wire, mattress spring wire, duct wire and specialist wires.',
        'The range serves different purchasing needs. A civil contractor may buy prestressing strand to a structural specification, while a conductor or spring manufacturer needs wire that meets the requirements of a downstream production process.'
    ],'industrial-hall','Illustrative wire production hall','/products/','Explore Essen Steel products'),
    feature('From strand to concrete span', [
        'Prestressing strand is used in concrete bridges, rail infrastructure and buildings. Steel core wire and strand reinforce ACSR conductors. Other wires serve fencing, agricultural, bedding, cable and industrial applications.',
        'In a viaduct, prestressing strand introduces compression into the concrete girders that span between piers. The design sets the strand specification. Essen’s other wire families serve different roles, from reinforcement within overhead conductors to wire formed into mattress springs.'
    ],'infra','Illustrative bridge infrastructure','/sectors/','Explore industries and applications'),
    feature('Match the wire to the work', [
        'Essen works with engineers, procurement teams and manufacturers to clarify order requirements. A useful enquiry covers the applicable standard, grade, dimensions, quantity, packaging and test documentation.',
        'For UAE or international enquiries, include the destination and required delivery date so the sales team can review the supply arrangements.'
    ],'hero','Illustrative steel strand close-up','/partnership/','Discuss a supply requirement'),
    feature('Kizad and Khalifa Port', [
        'Essen Steel manufactures in Kizad, Abu Dhabi, near Khalifa Port. The location supports road and sea freight planning for domestic and international enquiries.',
        'For export orders, give the destination, required delivery window and any packing or shipping document requirements so the team can discuss the applicable arrangements.'
    ],'audit-logistics','Illustrative coil shipment approaching a container logistics yard','/partnership/','Explore partnership and supply')
))
interior('partnership','Partnership and Supply','From the first specification discussion to delivery planning.',feature_group(
    feature('Send a complete enquiry', ['Start with the application and product designation. Add the standard, grade, dimensions, quantity and any requirements for testing, coating or documentation. If the specification is still being developed, share the operating conditions and decision timeline.'], 'hero','Illustrative steel strand','/products/','Find the product'),
    feature('Plan for receipt and handling', ['Tell us the delivery destination, required date and packaging format. Include unloading, storage or production-line constraints so those requirements can be considered before the order is confirmed.'], 'factory','Illustrative industrial reel handling','/contact/','Request a Quote')
))
policy_documents = '''<section class="catalogue-guide">
  <div><h2>Company and product literature</h2><p>Request the current company brochure or the low-relaxation PC strand brochure. For a purchase specification, ask for the applicable product data sheet and current standard.</p><a class="textlink" href="mailto:sales@essensteel.com?subject=Essen%20Steel%20brochure%20request">Request a brochure →</a></div>
  <div><h2>Quality, EHS and energy policies</h2><p>Request the current Quality, Environment, Health and Safety, or Energy Policy for supplier onboarding, prequalification or tender documentation.</p><a class="textlink" href="mailto:sales@essensteel.com?subject=Essen%20Steel%20policy%20request">Request a policy →</a></div>
</section>'''
interior('downloads','Technical Resources','Request product data sheets, policies and quality documentation.',feature_group(
    feature('Product data sheets', ['Share the product family and applicable standard or grade so the sales team can identify the relevant document. If comparing materials, use the same units and confirm that each data sheet covers the construction and dimensions you intend to order.'], 'pc','Illustrative steel strand detail','/products/','Browse the catalogue'),
    feature('Test reports and certificates', ['Specify which reports or certificates your purchase order or tender requires. Include the required test results, issuing body or approval scope where applicable.'], 'mill','Illustrative coil tag and inspection worksheet','mailto:sales@essensteel.com?subject=Product%20documentation%20request','Request documentation')
)+policy_documents)
interior('projects','Project Enquiries','Discuss wire and strand requirements for your project.',feature_group(
    feature('Start with the design requirement', ['Tell us what you are building, which product the design specifies and what standard applies. Include the project location, procurement stage, quantities and delivery timetable.'], 'infra','Illustrative infrastructure application','/sectors/','Browse applications'),
    feature('Prepare the procurement package', ['Share inspection or documentation requirements early, especially where a consultant or authority must review the material. Include packaging or handling constraints for staged deliveries.'], 'hero','Illustrative steel strand','/contact/','Discuss your project')
))
quote_products = ''.join(f'<option>{escape(name)}</option>' for name, *_ in products)
contact_content = f"""
<div class="contact-grid">
  <section id="quote" class="quote-panel">
    <span class="eyebrow">Sales enquiries</span>
    <h2 class="rule">Find out more</h2>
    <p>Tell us what you need. Include the specification and delivery requirements if you have them.</p>
    <form id="quote-form">
      <div class="quote-fields">
        <label>Name<input name="Name" autocomplete="name" required></label>
        <label>Company<input name="Company" autocomplete="organization" required></label>
        <label>Work email<input name="Work email" type="email" autocomplete="email" required></label>
        <label>Product<select name="Product"><option value="">Select a product</option>{quote_products}<option>Help me choose</option></select></label>
      </div>
      <label>Project or order details<textarea name="Project or order details" rows="5" placeholder="Application, grade or standard, quantity, destination and required date" required></textarea></label>
      <button class="button" type="submit">Email enquiry →</button>
    </form>
    <noscript><p>Email your enquiry to <a href="mailto:sales@essensteel.com">sales@essensteel.com</a>.</p></noscript>
  </section>
  <aside class="contact-aside">
    {photo('industrial-hall','Illustrative steel wire production hall','contact-photo')}
    <div class="contact-details">
      <h2>Talk to Essen Steel</h2>
      <p><a href="mailto:sales@essensteel.com">sales@essensteel.com</a><br><a href="tel:+97125109000">+971 2 510 9000</a></p>
      <h3>Abu Dhabi, UAE</h3>
      <address>KHIA4-18D, Kizad A<br>Al Taweelah, Abu Dhabi, UAE</address>
      <p><a href="https://www.google.com/maps/search/?api=1&amp;query=Essen+Steel+Industry+LLC+Abu+Dhabi">Find Essen Steel on the map →</a></p>
    </div>
  </aside>
</div>
<div class="catalogue-guide">
  <div><h2>Need technical documents?</h2><p>Share the product and governing standard or tell us which test report or certificate your project requires.</p><a class="textlink" href="/downloads/">Technical resources →</a></div>
  <div><h2>Discuss a supply requirement</h2><p>For staged deliveries or specialist handling, include the delivery window, packaging and receiving constraints in your enquiry.</p><a class="textlink" href="/partnership/">Partnership and supply →</a></div>
</div>
<script src="/assets/contact.js" defer></script>
"""
interior('contact','Contact Essen Steel','Speak to the sales team about a quote, product specification or delivery requirement.',contact_content)
interior('insights','Insights','Practical guides to steel strand and technical documentation.',stories_grid())
article_headings = {
    'pc-strand': ('How prestressing works', 'What to confirm before ordering'),
    'mill-test-report': ('Match the report to the material', 'Check the results against the order'),
}
for title, slug, img, desc, body in stories:
    headings = article_headings.get(slug)
    if headings:
        sentences = body.split('. ')
        split = 2 if slug == 'pc-strand' else 1
        first = '. '.join(sentences[:split]) + '.'
        second = '. '.join(sentences[split:])
        prose = f'<h2>{headings[0]}</h2><p>{escape(first)}</p><h2>{headings[1]}</h2><p>{escape(second)}</p>'
    else:
        prose = ''.join(f'<p>{escape(paragraph)}</p>' for paragraph in body.split('\n\n'))
    article = f"""
    <article class="wrap section insight-article">
      <header class="insight-article-header">
        <a class="textlink" href="/insights/">← All insights</a>
        <p class="eyebrow">Technical insight</p>
        <h1>{escape(title)}</h1>
        <p class="insight-lead">{escape(desc)}</p>
      </header>
      <figure class="insight-figure">{photo(img, 'Illustrative detail')}<figcaption>Illustrative image</figcaption></figure>
      <div class="insight-body">{prose}</div>
      <div class="insight-article-footer">
        <a class="textlink" href="/insights/">← All insights</a>
        {button('/downloads/', 'Technical Resources')}
      </div>
    </article>"""
    page('insights/'+slug,title,desc,article)
interior('privacy-policy','Privacy','Information for visitors to the Essen Steel website.','<p>When you email Essen Steel, we receive the contact information and enquiry details you provide.</p>')
interior('cookies','Cookies','Information for visitors to the Essen Steel website.','<p>This website uses no first-party cookies or analytics scripts. It requests the Exo typeface from Google Fonts.</p>')
interior('404.html','Page unavailable','The address may have changed.',button('/','Return to Home'))
