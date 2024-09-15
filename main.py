from requests import get, Session
from bs4 import BeautifulSoup
from pprint import pprint
import re

home = 'https://archives.doctsf.com'
target = 'https://archives.doctsf.com/documents/index.php?num_serie=172'
search_class = 'lien_neutre'

S = Session()

r = S.get(target)
# print(f'status_code = {r.status_code}')

b = BeautifulSoup(r.content, 'html.parser')
f = b.find_all(class_=search_class)

for found in f:
    s = str(found.extract()).split('"')[3]
    title = f'{found.text}'
    # print(f'********************\n{s}')
    o_r = S.get(f'{home}{s}')
    print(f'second_status_code = {o_r.status_code}')
    o_b = BeautifulSoup(o_r.content, 'html.parser')
    f2 = o_b.find('a', title='Imprimer')
    js_link = f2.find('a', href=re.compile(r"javascript:imprimer('./afficher_document.php?num_doc=102672&num_fic=1')"))
    
    # Vérifier s'il y a des liens correspondants
    if js_link:
        js_link = js_link[0]['href']
        match = re.search(r"javascript:imprimer('./afficher_document.php?num_doc=102672&num_fic=1')", js_link)
        if match:
            pdf_url = match.group(1)
            
            # Télécharger le fichier PDF
            pdf_response = get(pdf_url)
            
            # Enregistrer le PDF localement
            with open('document.pdf', 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            
            print("PDF téléchargé avec succès.")
        else:
            print("Lien JavaScript non trouvé.")
    else:
        print("Aucun lien JavaScript trouvé.")
        # l = S.get(str(f2).split('"')[3])
    # with open(f'{title}.pdf', 'wb') as f:
    #     f2.html.render(str(f2).split('"')[3])


 Electronique et Loisirs Magazine N°  1 - Mai 1999.pdf
