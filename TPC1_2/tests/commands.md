# Setup do flit e do projeto Python
flit build & flit install

# Comandos usando o wfreq 
wfreq -n tests/Camilo-Amor_de_Perdicao.md | more
                                          | grep '[A-Z][a-z]\+' 
                                          | grep -P '[A-Z][a-z]+' | sort -n 
                                          | rg '[A-Z]\w*'
                                          | rg -iw 'Não'
                                          | rg -iw 'Se'
      -m 20