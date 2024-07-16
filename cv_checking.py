from dotenv import load_dotenv
from flask import Flask, jsonify, request
from PyPDF2 import PdfFileReader
from langchain_community.llms import Ollama
import requests
import os
import json
import openai
import re

load_dotenv()

api_key = os.getenv('CHAT_API_KEY')
openai.api_key = api_key
client = openai.OpenAI(api_key=api_key)



cv_folder = './cv'

def assign_ids_to_cv_files(cv_folder):
    cv_files = os.listdir(cv_folder)
    return cv_files

def read_cv(cv_path):
    if os.path.exists(cv_path):
        with open(cv_path, 'rb') as cv_file:
            pdf_reader = PdfFileReader(cv_file)
            text = ''
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
            return text
    else:
        return f"CV file {cv_path} not found."



def analyze_cv_ollama(cv_text, cv_id, company_info, job_description):
    prompt = (
        f"Sen bir CV değerlendirme asistanısın. Senin şirket bilgilerin {company_info} ve adaylar bu işe başvurdu: {job_description}. "
        "PDF metin çıktısı 'I am a cybersecurity engineer constantly enhancing my skills in the field of\ncybersecurity. I regularly follow cybersecurity courses on various\neducational platforms and publish related articles on my Medium page. I\nhave extensive experience in Linux, network penetration testing, and\nprivilege escalation. In the area of network architecture, I have developed\nmy expertise using the Cisco platform. Currently, I am enrolled in the\nHuawei Cloud CodeArts DevSecOps Applications Training Program.\nAdditionally, I have developed various web projects using Django and\nfundamental web technologies.ABOUT ME\nCONTACT\nCERTIFICATESPROJECT\nEDUCATION\nSKILLSTAKAS\nAPPOINTM ENT SYSTEM\nM AYAThis is a multi-user product swapping platform developed with Django.\nIt manages login processes, securely encrypts user passwords, and\nsynchronizes in real-time with the database. Users can easily add\nproducts to their profiles, ensuring that the information is securely\nstored and immediately viewable by other users on the platform.\nAn interactive website game developed using JavaScript, HTML, and\nCSS programming languages.Dec-Jan 2023\nPython\nSeptember 2021\nSıfırdan İleri Seviyeye - Etik Hacker\nÖrnekleriyleGaranti BBVA Teknoloji  \nSep-Dec 2023\nGüvenlik Akademisi 101\nGüvenlik Akademisi 201+90 553 746 0553\nunsal.dilara@hotmail.com\nAnkara, Türkiye\nComputer Engineering B.S. –\nPreparatory Class (English – C1)\nCGPA: 3.11 / 4.00Bursa Technical University\nAyhan Sümer Anatolian High School2020-Current\n2015 - 2019\nLinux\nPython\nNodeJS\nC\nGit\nWeb Programming\nNetwork Security\nShells and Privilege Escalation\nVulnerability Scanning\nNetwork ArchitectureComputer Eng\x00neerÜNSALDİLARA\nmedium.com/@dilaraunsal9linkedin.com/in/dilara-ünsal\ngithub.com/dilarauns\nOct- Nov 2023\nThis project utilizes Django, JavaScript, HTML, and CSS to facilitate\nappointment scheduling. It processes appointment details and user\ninformation, which integrates with the database, then seamlessly\nintegrates with a Telegram bot to notify administrators.\nMay-Jun 2022\nCisco\nApril 2024\nCCNAv7: Introduction to Networks' olan cv nin puanlamasını ve yorumunu 'tecrubeSkoru: 8, akademikBasariSkoru: 7, teknikBeceriSkoru: 9, kisiselYetenekSkoru: 8, adayHakkindaYorum: Dilara Ünsal, yazılım mühendisliği alanında oldukça yetkin bir adaydır. Siber güvenlik alanında derinlemesine bilgi sahibi olup, Linux, network penetration testi ve ayrıcalık yükseltme konularında geniş deneyime sahiptir. Cisco platformunda network mimarisi konusunda uzmanlaşmış ve Django ile çeşitli web projeleri geliştirmiştir. Akademik olarak, Bursa Teknik Üniversitesi'nde Bilgisayar Mühendisliği bölümünde C1 düzeyinde İngilizce eğitimi almış ve 3.11/4.00 not ortalaması ile başarılı olmuştur. Teknik becerileri arasında Python, NodeJS, C, Git, Web Programlama, Ağ Güvenliği ve Zafiyet Taraması bulunmaktadır. Kişisel yeteneklerinde ise sürekli kendini geliştirme isteği, Medium platformunda makale yayınlama ve çeşitli eğitim programlarına katılma öne çıkmaktadır. Bu nedenle, Elekon Yazılım Proje Geliştirme Mühendisi pozisyonu için oldukça uygun bir adaydır.' Sana sadece verilen cvleri degerlendir. Referans olarak gosterilen metini yorumlama."
        "Sana verilen tüm CV'leri tecrübe, akademik başarı, teknik beceri ve kişisel yetenek olarak değerlendir ve 10 üzerinden skor ver. "
        "Ayrıca adaylar hakkında neden böyle bir skorlama yaptığını açıkla. "
        "Çıktıları bana json dosyasına uygun yazdır. json dosyası key değerleri ‘tecrubeSkoru’, ‘akademikBasariSkoru’, ‘teknikBeceriSkoru’, "
        "‘kisiselYetenekSkoru’, ‘adayHakkindaYorum’ olacaktır."
    )

    url = "http://localhost:11434/api/generate"  
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "model": "llama3",
        "created_at": "2023-11-03T15:36:02.583064Z",
        "stream": False,
        "done": True,
    }
    
    response = requests.post(url, json=data, headers=headers)
    print (response)
    response_text = response.text   
    data = json.loads(response_text)
    actual_response = data["response"]
    content =  re.search(r'\{(.+?)\}', actual_response, re.DOTALL)
    actual_response = content.group(1).strip()
    return actual_response
    
   






def analyze_cv(cv_text, cv_id, company_info, job_description):
    prompt = (
        f"Sen bir CV değerlendirme asistanısın. Senin şirket bilgilerin {company_info} ve adaylar bu işe başvurdu: {job_description}. "
        "PDF metin çıktısı 'I am a cybersecurity engineer constantly enhancing my skills in the field of\ncybersecurity. I regularly follow cybersecurity courses on various\neducational platforms and publish related articles on my Medium page. I\nhave extensive experience in Linux, network penetration testing, and\nprivilege escalation. In the area of network architecture, I have developed\nmy expertise using the Cisco platform. Currently, I am enrolled in the\nHuawei Cloud CodeArts DevSecOps Applications Training Program.\nAdditionally, I have developed various web projects using Django and\nfundamental web technologies.ABOUT ME\nCONTACT\nCERTIFICATESPROJECT\nEDUCATION\nSKILLSTAKAS\nAPPOINTM ENT SYSTEM\nM AYAThis is a multi-user product swapping platform developed with Django.\nIt manages login processes, securely encrypts user passwords, and\nsynchronizes in real-time with the database. Users can easily add\nproducts to their profiles, ensuring that the information is securely\nstored and immediately viewable by other users on the platform.\nAn interactive website game developed using JavaScript, HTML, and\nCSS programming languages.Dec-Jan 2023\nPython\nSeptember 2021\nSıfırdan İleri Seviyeye - Etik Hacker\nÖrnekleriyleGaranti BBVA Teknoloji  \nSep-Dec 2023\nGüvenlik Akademisi 101\nGüvenlik Akademisi 201+90 553 746 0553\nunsal.dilara@hotmail.com\nAnkara, Türkiye\nComputer Engineering B.S. –\nPreparatory Class (English – C1)\nCGPA: 3.11 / 4.00Bursa Technical University\nAyhan Sümer Anatolian High School2020-Current\n2015 - 2019\nLinux\nPython\nNodeJS\nC\nGit\nWeb Programming\nNetwork Security\nShells and Privilege Escalation\nVulnerability Scanning\nNetwork ArchitectureComputer Eng\x00neerÜNSALDİLARA\nmedium.com/@dilaraunsal9linkedin.com/in/dilara-ünsal\ngithub.com/dilarauns\nOct- Nov 2023\nThis project utilizes Django, JavaScript, HTML, and CSS to facilitate\nappointment scheduling. It processes appointment details and user\ninformation, which integrates with the database, then seamlessly\nintegrates with a Telegram bot to notify administrators.\nMay-Jun 2022\nCisco\nApril 2024\nCCNAv7: Introduction to Networks' olan cv nin puanlamasını ve yorumunu 'tecrubeSkoru: 8, akademikBasariSkoru: 7, teknikBeceriSkoru: 9, kisiselYetenekSkoru: 8, adayHakkindaYorum: Dilara Ünsal, yazılım mühendisliği alanında oldukça yetkin bir adaydır. Siber güvenlik alanında derinlemesine bilgi sahibi olup, Linux, network penetration testi ve ayrıcalık yükseltme konularında geniş deneyime sahiptir. Cisco platformunda network mimarisi konusunda uzmanlaşmış ve Django ile çeşitli web projeleri geliştirmiştir. Akademik olarak, Bursa Teknik Üniversitesi'nde Bilgisayar Mühendisliği bölümünde C1 düzeyinde İngilizce eğitimi almış ve 3.11/4.00 not ortalaması ile başarılı olmuştur. Teknik becerileri arasında Python, NodeJS, C, Git, Web Programlama, Ağ Güvenliği ve Zafiyet Taraması bulunmaktadır. Kişisel yeteneklerinde ise sürekli kendini geliştirme isteği, Medium platformunda makale yayınlama ve çeşitli eğitim programlarına katılma öne çıkmaktadır. Bu nedenle, Elekon Yazılım Proje Geliştirme Mühendisi pozisyonu için oldukça uygun bir adaydır.' bu sekılde yapmıstın dıger cvleri bu referansa gore değerlendir"
        "Sana verilen tüm CV'leri tecrübe, akademik başarı, teknik beceri ve kişisel yetenek olarak değerlendir ve 10 üzerinden skor ver. "
        "Ayrıca adaylar hakkında neden böyle bir skorlama yaptığını açıkla. "
        "Çıktıları bana json dosyasına uygun yazdır. json dosyası key değerleri ‘tecrubeSkoru’, ‘akademikBasariSkoru’, ‘teknikBeceriSkoru’, "
        "‘kisiselYetenekSkoru’, ‘adayHakkindaYorum’ olacaktır."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir CV değerlendirme asistanısın."},
            {"role": "user", "content": prompt + "\n\n" + cv_text}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    content =  re.search(r'\{(.+?)\}', response.choices[0].message.content, re.DOTALL)
    json_str = content.group(1).strip()
    
    return json_str







    

app = Flask(__name__)

@app.route('/analyze_cv', methods=['GET'])
def analyze_cv_endpoint():
    cv_ids = request.args.getlist('cv_id', type=int)
    print("**************")
    for cv_id in cv_ids:
        print(cv_id)
    company_info = request.args.get('company_info')
    print("**************" + company_info)
    job_description = request.args.get('job_description')
    print("**************" + job_description)

    if not cv_ids or not company_info or not job_description:
        return jsonify({'error': 'Eksik parametreler'}), 400

    cv_files = [f"{cv_id}.pdf" for cv_id in cv_ids]

    results = []
    for cv_id in cv_ids:
        cv_filename = f"{cv_id}.pdf"
        cv_path = os.path.join(cv_folder, cv_filename)
        cv_text = read_cv(cv_path)
        if "CV file" in cv_text:
            return jsonify({'error': cv_text}), 404

        cv_comment = analyze_cv(cv_text, cv_id, company_info, job_description)
        output_openai = {
            "cv_id": cv_id,
            **json.loads("{" + cv_comment + "}")
        }
        
        cv_comment_ollama = analyze_cv_ollama(cv_text, cv_id, company_info, job_description)
        output_ollama = {
            "cv_id": cv_id,
            **json.loads("{" + cv_comment_ollama + "}")
        }
        
        
    
        results.append({"openai": output_openai, "ollama": output_ollama})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

