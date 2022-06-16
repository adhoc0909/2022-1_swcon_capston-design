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


			[그림-1]
