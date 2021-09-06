from flask import Flask, render_template, request
import src as algo

app = Flask(__name__)

@app.route('/' , methods=["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=["GET", "POST"])
def encrypt():
    if (request.method == "POST"):
        file = request.files['fileInput']
        if file.filename == '':
            cypher = request.form['methodInput']
            text = request.form['plaintextInput'].lower().replace(" ","")
            key = request.form['keyInput'].lower().replace(" ","")
            m = int(request.form['key-m'])
            b = int(request.form['key-b'])
            if (cypher=="vigenere"): 
                cytext = algo.vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="full-vigenere"):
                cytext = algo.full_vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="autokey-vigenere"):
                cytext = algo.autokey_vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="playfair"):
                playfairkey = key.replace('j','')
                pfkey = algo.playfairkeymaker(playfairkey)
                pftext = algo.playfairtextmaker(text)
                pfresult = algo.playfair(pftext,pfkey,True)
                encrypted1 = ""
                for elements in pfresult:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="affine"):
                cytext = algo.affine_encrypt(text,m,b)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
        else:
            filetext = file.read().decode("utf-8").split("\r\n")
            text = filetext[0].lower().replace(" ","")
            key = filetext[1].lower().replace(" ","")
            m, b = 0, 0
            if (len(filetext)>2):
                m = int(filetext[2])
                b = int(filetext[3])
            cypher = request.form['methodInput']
            if (cypher=="vigenere"): 
                cytext = algo.vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="full-vigenere"):
                cytext = algo.full_vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="autokey-vigenere"):
                cytext = algo.autokey_vigenere_encrypt(text,key)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="playfair"):
                playfairkey = key.replace('j','')
                pfkey = algo.playfairkeymaker(playfairkey)
                pftext = algo.playfairtextmaker(text)
                pfresult = algo.playfair(pftext,pfkey,True)
                encrypted1 = ""
                for elements in pfresult:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
            elif (cypher=="affine"):
                cytext = algo.affine_encrypt(text,m,b)
                encrypted1 = ""
                for elements in cytext:
                    encrypted1 += chr(elements+97)
                encrypted = algo.outputmaker(encrypted1)
                with open("result.txt", "w") as fo:
                    fo.write(encrypted)
                return render_template("index.html", answer = encrypted, mode = "encrypted")
    else:
        return render_template("index.html")

@app.route('/decrypt', methods=["GET", "POST"])
def decrypt():
    if (request.method == "POST"):
        cypher = request.form['methodInput']
        encrypted = request.form['cyphertextInput'].lower().replace(" ","")
        key = request.form['keyInput'].lower().replace(" ","")
        m = int(request.form['key-m'])
        b = int(request.form['key-b'])
        if (cypher=="vigenere"):
            decryptedtext = algo.vigenere_decrypt(encrypted,key)
            decrypted = ""
            for elements in decryptedtext:
                decrypted += chr(elements+97)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
        elif (cypher=="full-vigenere"):
            decryptedtext = algo.full_vigenere_decrypt(encrypted,key)
            decrypted = ""
            for elements in decryptedtext:
                decrypted += chr(elements+97)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
        elif (cypher=="autokey-vigenere"):
            original = request.form['originalInput']
            ptext = algo.autokey_vigenere_decrypt(original,encrypted,key)
            decrypted = ""
            for elements in ptext:
                decrypted += chr(elements+97)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
        elif (cypher=="playfair"):
            playfairkey = key.replace('j','')
            pfkey = algo.playfairkeymaker(playfairkey)
            pfdecrypt = algo.playfair(algo.playfairtextmaker(encrypted),pfkey,False)
            decrypted1=""
            for elements in pfdecrypt:
                decrypted1 += chr(elements+97)
            decrypted = decrypted1.replace("x","")
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
        elif (cypher=="affine"):
            ptext = algo.affine_decrypt(encrypted,m,b)
            decrypted = ""
            for elements in ptext:
                decrypted += chr(elements+97)
            return render_template("index.html", answer1 = decrypted, mode= "decrypted")
    else:
        return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)