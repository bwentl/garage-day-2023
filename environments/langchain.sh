# this environment is based off of one used by text-generation-webui
# several packages were used to extend the functionality for 
# langchain, GPTQ, 
conda remove --name langchain --all
conda create -n langchain python=3.10.9 -y
conda activate langchain
conda install -y pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
# requirements for text-generation-webui
cd tools/text-generation-webui
pip install -r requirements.txt
cd ../..
# requirements for lora peft model
cd tools/alpaca-lora
pip install -r requirements.txt
cd ../..
# requirements for GPTQ for llama
cd tools/GPTQ-for-LLaMa
git checkout cuda
git pull
python setup_cuda.py install
cd ../..
# install dev version of transformers
cd packages/transformers
pip install cmake lit
pip install --editable . --force-reinstall
cd ../..
# install dev version of langchain
cd packages/langchain
pip install --editable . --force-reinstall
cd ../..
# install additional packages used by langchain
conda install -y poppler
conda install -y pytesseract
pip install numexpr
pip install sentence_transformers
# pip install InstructorEmbedding  # not supported by langchain
pip install chromadb
pip install redis
pip install unstructured
pip install unstructured[local-inference]
pip install 'git+https://github.com/facebookresearch/detectron2.git'
# 20230407 patch, download problematic packages
pip install protobuf==3.19.5 --force-reinstall
pip install tensorboard==2.8.0 --force-reinstall
pip install argilla==1.5 --force-reinstall
# for additional langchain tools
pip install google-api-python-client
# install llama cpp connector
pip install git+https://github.com/abetlen/llama-cpp-python.git
# install pgvector used for long term memory
pip install pgvector
# sudo apt-get update -y && sudo apt-get install libpq-dev
pip install psycopg2
# openai python wrapper
pip install openai