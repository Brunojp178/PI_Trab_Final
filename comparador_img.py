import cv2, math, os
from matplotlib import pyplot as plt

def compararImg(imgX, imgY):

  imgY = cv2.resize(imgY,(240, 240))

  color = ('b', 'g', 'r')

  for i, col in enumerate(color):
    hist1 = cv2.calcHist([imgX], [i], None, [256], [0,256])
    plt.plot(hist1, color = col)
    plt.xlim([0, 256])

  for i, col in enumerate(color):
    hist2 = cv2.calcHist([imgY], [i], None, [256], [0,256])
    plt.plot(hist2, color = col)
    plt.xlim([0, 256])

  correl = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
  chisquare = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
  bhatta = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)

  r = math.sqrt(math.pow(correl, 2) + math.pow(chisquare, 2) + math.pow(bhatta, 2))
  return int(r)

def main():

  arquivos = os.listdir('C:/Users/Rayanne/Desktop/IF/PI/Projeto Final/teste')

  caminho_item0 = 'C:/Users/Rayanne/Desktop/IF/PI/Projeto Final/teste/' + arquivos[0]
  image0 = cv2.imread(caminho_item0)
  image0 = cv2.resize(image0, (240, 240))


  resultados = []

  for i in range(1,len(arquivos)):
    caminho_item = 'C:/Users/Rayanne/Desktop/IF/PI/Projeto Final/teste/' + arquivos[i]
    image = cv2.imread(caminho_item)
    resultados.insert(i-1, compararImg(image0, image))

  ##for i in range(0,len(resultados)):
   ## print("Comparação entre imagem 1 e a imagem" , i+2, ":", resultados[i])


  menorDistancia = resultados[0]
  posicao = 0

  for i in range(0, len(resultados)):
    if (menorDistancia > resultados[i]):
      menorDistancia = resultados[i]
      posicao = i

  #print(menorDistancia)


main()
