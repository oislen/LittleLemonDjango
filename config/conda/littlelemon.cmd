:: list all available conda environments
call conda env list

:: create and activate new environment
call conda deactivate
call conda env remove --name littlelemon
call conda env list
call conda create --name littlelemon python=3.12 --yes
call conda activate littlelemon
call conda list

:: install all relevant python libraries
call pip install -r ..\requirements.txt

:: list all installed libraries
call conda list

:: export to yml file
:: call conda env export > littlelemon.yml
:: call conda env create -f littlelemon.yml
