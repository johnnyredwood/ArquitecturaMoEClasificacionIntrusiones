Arquitectura Mixture of Experts para Clasificación de Ataques en Dataset con Desbalance Extremo de Clases
Autor: John Ochoa Abad
Link Github: https://github.com/johnnyredwood/ArquitecturaMoEClasificacionIntrusiones

Lista de librerías y dependencias a instalar previamente para la ejecución:

scikit-learn
pyTorch
matplotlib
numpy
pandas
gc 
seaborn
pathlib
imbalanced-learn
scipy
xgboost
json
itertools
fast-api

El presente repositorio consiste en un serie de notebooks y .py para el desarrollo de un proyecto de clasificación de intrusiones en el dataset CIDS2017 de la Universidad de New Brunswick. Al estar el código basado en Python se debe tener un ambiente de ejecución habilitado para dicho lenguaje de programación. Para la ejecución del mismo y el reconocimiento del objetivo de cada archivo a continuación se indican una serie de pasos en el orden a seguir:

0. Como paso 0 es necesario clonar el repositorio y posteriormente generar dentro una carpeta llamada "Dataset". Dentro de dicha carpeta se deben colocar los archivos .csv descargados del siguiente link "https://cicresearch.ca/CICDataset/CIC-IDS-2017/", los cuales contienen los datos de las muestras previo limpieza de tráfico benigno e intrusiones. Dicho dataset es propiedad de la Universidad de New Brunswick.
1. Ejecutar celda a celda el archivo DataExploration.ipynb el cual consiste en la preparación y preanálisis inicial de los datos.
2. Ejecutar celda a celda el arhivo DataPreprocessing.ipynb el cual consiste en la limpieza del dataset previo a la ejecución de los modelos de Machine Learning.
3. Ejecutar celda a celda el arhivo BaselineModelsDataPreparation.ipybn el cual consiste en un archivo que contiene todos los procesos para terminar de preparar los datos y ejecuta pasos iniciales del pipeline para el entrenamiento de los modelos base.
4. Ejecutar celda a celda los archivos BaselineModelsRandomForest.ipynb, BaselineModelsXGBoost.ipynb, BaselineModelsNeuralNetwork.ipynb en el orden deseado. Cada uno corre los experimentos para los modelos base de tipo Random Forest, XGBoost y Neural Networks respectivamente.
5. Ejecutar celda a celda los archivos MixtureOfExpertsFirstArchitecture.ipynb, MixtureOfExpertsSecondArchitecture.ipynb, MixtureOfExpertsThirdArchitecture.ipynb. Para visualizar como los modelos van mejorando se recomienda ejecutar en orden las arquitecturas.

Una vez ejecutados los archivos para la obtención de una API se tiene el archivo adicional IntrusionDetectionAsAService.py el cual se corre directamente y se puede reconfigurar apuntando a cualquier modelo generado para con el mismo obtener una API de tipo predicción la cual puede implementarse en cualquier aplicación o sistema que requiera detección de intrusiones.

Al ejecutar de manera correcta los archivos se generarán carpetas de subsets en donde se irán depositando archivos de tipo .joblib de datasets procesados que posteriormente se usarán en los procesos subsecuentes de entrenamiento, validación y testing de los modelos, dichas carpetas tendrán el prefijo de Sets*. A su vez, se generarán carpetas con el formato Models* donde se irán depositando los modelos generados para las arquitecturas Mixture of Experts para los expertos, el gating y la arquitectura compuesta final. Por último, se generarán carpetas con formato Logs* los cuales incluirán archivos .log con métricas y reportes de clasificación de los modelos aplicados sobre sets de validación y testing, a su vez en dichas carpetas se depositaran archivos de formato .png de las matrices de confusión generadas de igual manera para ejecuciones de los modelos base y de tipo Mixture of Experts sobre los sets de validación y de testing.