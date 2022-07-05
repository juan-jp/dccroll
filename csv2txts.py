
text = open("fortraining.txt", "r",encoding= "utf8")
  
# joining with space content of text
text = ' '.join([i for i in text])  
  
# replacing ',' by space
text = text.replace(",", ":")
text= text.replace(":", "\n"+":")
with open('fortraining copy.txt', 'w', encoding='utf8') as f:
    f.write(text)
"""text_file_path = 'fortraining copy.txt'
new_text_content = ''
with open(text_file_path,'r', encoding="utf8") as f:
    lines = f.readlines()
    for i, l in enumerate(lines):
        if (i%2)==0:
            new_string= l.replace( ":", "").strip()
        else:
            new_string= new_string
        
        if new_string:
            new_text_content += new_string + '\n'
        else:
            new_text_content += '\n'
                
with open(text_file_path,'w',encoding= "utf8") as f:
    f.write(new_text_content) """

