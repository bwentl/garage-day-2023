# this environment is based off of one used by text-generation-webui
# several packages were used to extend the functionality for 
# langchain, GPTQ, 
conda remove --name langchain --all
conda create -n langchain python=3.10.9 -y
conda activate langchain
pip install torch torchvision torchaudio
pip install transformers
pip install peft
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
# gradio ui
pip install gradio