# 2022년 1학기 소프트웨어융합 캡스톤디자인
## GAN 기반 Data Augmentation을 통한 흉부 X-ray 사진 classification 성능 개선
---
## 1. 과제 개요
---
### 가. 과제 설계 배경 및 필요성
 최근 딥러닝을 통한 이미지 분류 task가 활발히 연구되고 있지만, 이는 데이터셋이 충분하지 않거나 클래스 간 불균형이 존재할 경우 좋은 모델을 적용하여도 과적합 발생 등의 이유로 그에 준한 성능을 내지 못할 수 있다. 특히 의료 데이터의 경우 클래스 불균형이 발생하는 경우가 종종 발생한다. 예컨대 흉부 x-ray의 경우 흔한 증상의 경우 클래스에 속한 데이터셋이 많은 반면, 희귀한 증상 클래스에 속한 데이터셋은 적은 경우가 그 경우다. 이를 해결하기 위해 클래스 불균형을 야기하는 클래스에 대한 데이터셋을 추가로 확보하는 방법이 있지만, 실제 데이터셋을 확보하는 것에 어려움을 겪는 경우가 있기 때문에 data augmentation 기법을 사용하여 클래스 간의 균형을 맞추는 작업을 수행할 필요가 있다. 따라서 본 과제에서는 클래스 불균형이 존재하는 흉부 X-ray 이미지 데이터셋에 대해 Data Augmentation 기법을 활용하여 분류 모델의 성능을 올리는 것에 중점을 두고 연구를 진행하였다.
 
### 나. 과제 주요 내용

  본 과제는 클래스 불균형이 존재하는 흉부 X-ray 이미지 데이터셋으로 이미지상의 병리학적 증상(pathology) 유무 여부를 분류하는 모델의 분류 성능을 data augmentation 기법을 통해 개선하는 것을 목표로 한다. 
 
 데이터셋으로 stanford 병원에서 민간에 연구용으로 공개한 CheXpert 데이터셋을 사용하였다. 해당 데이터셋은 224,316장의 이미지로 구성되며, 각 이미지에는 14개의 클래스(병리학적 증상) 중 각 클래스의 양/음성 여부를 나타내는 정보가 레이블링이 되어 있다. 이 데이터셋을 가지고 사전 학습된 DenseNet-121 모델을 전이학습을 한다. 학습된 모델의 분류 성능을 baseline으로 두어, data augmentation을 한 후의 분류 성능과 비교하여 개선도를 체크하는 것이 본 과제의 최종 결과이다. 이때 분류 성능 지표로 해당 데이터셋의 클래스 불균형을 초래하는 세 가지 클래스에 대한 ROC(Receiver Operating Characteristic)의 AUC(Area Under the Curve)를 사용한다. 해당 세 가지 클래스는 아래 [그림-1]에 나와있는 바와 같이 Positive 비율이 5% 미만인 클래스 Lung Lesion, Pleural Other, Fracture이다. 
 
 Data Augmentation 기법으로 Generative Adversarial Networks를 사용한다. GAN 모델로는 고해상도의 이미지를 안정적인 학습을 통해 생성해내는 것으로 알려진 Progressive Growing Generative Adversarial Networks를 채택하였다. [1]에서는 본 프로젝트와 동일한 GAN 모델로 분류 모델 성능을 개선하는데 성공하였고, 본 프로젝트에서는 [1]에서 개선된 양보다 더 개선시키는 것을 목표로 한다. 그 방법으로 GAN 학습에 사용되는 데이터셋을 Filtering에 기반한 Data Augmentation(Gaussian Blur, Unsharp Masking, Minimum Filtering)[2]으로 데이터셋을 증강하여 GAN을 학습한다. 이 경우 GAN의 학습이 더 잘 될 것으로 기대되어, 이는 분류 모델 학습 시 좋은 질의 fake image의 유입으로 인한 성능 개선으로 귀결이 될 것으로 기대하고 진행하였다. 
 
![image](https://user-images.githubusercontent.com/52408669/174017250-2dbee843-0bf5-46c4-97b2-3d27df6b5f2d.png)


[그림-1]


---
## 2. 최종 결과물 목표

  세 가지 클래스(Lung Leison, Pleural Other, Fracture)의 AUC 점수가 augmentation을 하기 전보다 개선됨을, 그리고 [1]에서 제시한 점수보다 개선됨을 최종 정량적 목표로 설정하였다. 
  
 
---
## 3. 모델 개요
---
### 가. Classificatoin Model
classifier 모델로 DenseNet-121을 사용하였다. 사전 학습이 된 모델을 전이학습을 통해 학습을 진행하였다. 
![image](https://user-images.githubusercontent.com/52408669/174018174-9bc57ed8-2a78-419b-8f11-1c4fffb92f65.png)

### 나. GAN Model
GAN 모델로 PGGAN(Progressive Growing Generative Adversarial Networks)을 사용하였다. 해당 모델은 해상도를 점차 저해상도에서 고해상도로 올려가며 최종적으로 고해상도의 이미지를 안정적으로 학습을 진행할 수 있는 모델이다. 
Generator와 Discriminator은 서로 대칭적인 구조를 가지고 있으며, 4X4 해상도 층에서 시작하여 최종적으로 training dataset의 이미지 해상도까지 도달한다.
![image](https://user-images.githubusercontent.com/52408669/174018778-2e1275b5-2edb-44b5-a562-716d7e9625b1.png)

---
## 4. 수행 결과
---
### 가. 과제수행 결과
 본 과제에서 결과로 제시하는 지표는 직접 분류 모델을 augmentation 없이 학습시킨 AUC 점수와 augmentation 후에 학습시킨 AUC 점수를 비교하여 나타낸 개선율과, 논문의 개선율과 본 과제의 개선율을 비교한 결과이다. 아래 표의 행은 데이터셋의 크기에 따른 세 가지 클래스의 AUC 점수를 나타낸 것이며, 열은 다음과 같다. 
Pathology: 클래스
논문(no augmentation): 논문에서 augmentation 없이 학습시킨 분류 모델의 AUC 점수
논문(GAN augmentation): 논문에서 GAN으로 augmentation를 한 후 학습시킨 분류 모델의 AUC 점수
성능 향상(논문): 논문에서의 성능 향상
나(no augmentation): 본 과제에서 진행한 augmentation 없이 학습시킨 분류 모델의 AUC 점수
나(GAN augmentation): 본 과제에서 진행한 GAN으로 augmentation을 한 후 학습시킨 분류 모델의 AUC 점수
성능향상(나): 본 과제에서의 성능 향상

 ![image](https://user-images.githubusercontent.com/52408669/174019091-7673e9d2-e7d4-42fc-a486-44164f317d4e.png)
 
성능 향상(나)의 AUC 점수는 논문보다 개선율이 높으면 빨간색, 낮으면 파란색으로 표기하였다. 총 12개의 개선율 중 8개의 개선율이 논문보다 높았다.

### 나. 최종 결과물  주요 특징 및 설명
 위의 결과물 표에서는 전반적으로 논문보다 우수한 AUC 점수 개선을 보였고, 특히 주목할 점은 데이터셋이 100%일 때의 AUC 점수 개선율이다. [1]에서는 데이터셋이 커질수록 오히려 GAN을 통한 AUC 점수 개선이 되지 않고 낮아지는 경우가 발생한다고 언급하였고, 실제로 데이터셋이 100% 때의 논문의 개선율을 보면 오히려 낮아진 모습을 볼 수 있다. 반면 본 과제에서 진행한 결과 100%의 세 클래스 모두 AUC 점수가 떨어지지 않고 개선된 결과를 확인할 수가 있다. 

따라서 GAN 학습 시 filtering에 기반한 Data Augmentation을 통해 GAN 학습을 강화시킨 것의 효과를 입증하였다.
 
---
## 5. 기대 효과 및 활용방안
---
### 가. 기대효과
본 과제에서 수행한 결과물을 온전히 의료 진단에 사용하기에는 무리가 있으나, 의료 영상을 통한 진단 시 진료인의 참고 도구가 될 수 있따는 점에서 기대효과를 갖는다.

### 나. 활용방안
의료업 종사자의 진단 보조 시스템에 본 모델을 추가하여 흉부 X-ray를 통한 진단 시 참고자료로 사용할 수 있을 것이라 생각된다. 

---
## 6. 결론 및 제언 
본 과제에서는 GAN 기반 Data Augmentation 과제를 수행하기 위해 GAN 학습에 사용할 데이터를 Filtering에 기반한 Data Augmentation을 수행하였고, Filtering 기반 Augmentation을 하지 않은 결과보다 성능이 증가했다는 것에 의의가 있다. 의료 영상의 특성 상 Data Augmentation 수행 시 transformation 방법을 신중하게 골라야 한다는 점에서 연구 가치가 있다고 생각된다. 따라서 추후 연구에서는 의료 영상 GAN 학습을 위한 Data Augmentation 기법들이 연구가 된다면 클래스 불균형의 상황에서 더욱 높은 분류 모델의 성능을 얻을 수 있을 것이라 생각된다. 

---
[참고자료]
[1] Shobhita Sundaram, Neha Hulkund. 2021. GAN-based Data Augmentation for Chest X-ray Classification. KDD 2021

[2] Prasanth Ganesan, Sivaramakrishn an Rajaraman, L. Rodney Long, Behnaz Ghoraani, Sameer K. Antani 2019. Assessment of Data Augmentation Strategies Toward Performance Improvement of Abnormality Classification in Chest Radiographs. EMBC 2019.

[3] Tianyu Han, Sven Nebelung, Christoph Haarburger, Nicolas Horst, Sebastian Reinartz, Dorit Merhof, Fabian Kiessling, Volkmar Schulz, and DanielTruhn. 2019. Breaking Medical Data Sharing Boundaries by EmployingArtificial Radiographs. bioRxiv (2019).
