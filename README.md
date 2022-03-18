# 1. setup
`$ sh setup.sh`
모델 다운로드

# 2. 실행
`$ python3 pose_estimation.py`
default는 동영상이 실행 됨.

볼드체가 디폴트값

* --model : [**movenet_lightning**, movenet_thunder, posenet]
* --input_type : [**webcam**, video, image]
* --input_data : 입력 데이터 파일 (webcam은 안해도 됨)
* --save_result : 분석 결과 저장 여부 (True / False)
webcam으로 할려면  
`$ python3 pose_estimation.py --input_type webcam`



