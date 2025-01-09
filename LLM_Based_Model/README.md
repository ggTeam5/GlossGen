# add API key locally (WSL)

- get API key from https://platform.openai.com

- execute in terminal (please replace <your_api_key> with your own!):  
```
echo 'export OPENAI_API_KEY="<your_api_key>"' >> ~/.zshrc
source ~/.zshrc 
```

- You might want to run the last line seperately, if you already have a correct api key written in ~/.zshrc

# execute model
the specified language will be used for the prompts and for the ouput file name
```
python3 main.py <language> <path to training file> <path to test file>
```