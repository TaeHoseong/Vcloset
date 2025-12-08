# 👗 VCloset – AI Virtual Try-On 기반 중고 패션 스토어  
Vcloset은 강력한 AI기술을 기반으로 내 사진 위에 원하는 상품을 가상으로 입혀볼 수 있는 플랫폼입니다!
  
🔥🔥 https://vcloset.netlify.app 🔥🔥

## 🖼 데모 이미지
<table>
<tr>
  <th>Person</th>
  <th>Garment</th>
  <th>Virtual Try On</th>
</tr>

<tr>
  <td><img src="demo/p1.png" height=300></td>
  <td><img src="demo/g1.png" height=300></td>
  <td><img src="demo/r1.png" height=300></td>
</tr>

<tr>
  <td><img src="demo/p1.png" height=300></td>
  <td><img src="demo/g2.png" height=300></td>
  <td><img src="demo/r2.png" height=300></td>
</tr>

<tr>
  <td><img src="demo/p1.png" height=300></td>
  <td><img src="demo/g3.png" height=300></td>
  <td><img src="demo/r3.png" height=300></td>
</tr>
</table>

## 📌 1. 프로젝트 소개

**VCloset**은 사용자가 직접 업로드한 전신 사진 위에  
원하는 상품을 입혀볼 수 있는 **AI Virtual Try-On 기반 리셀 서비스**입니다.

중고 거래에서는 사이즈 미스 때문에 환불/교환이 불가능한 경우가 많고,  
사진만 보고는 “내 체형에 어울릴까?”를 판단하기 어렵다는 문제점을 해결하기 위해 제작했습니다.

사용자는 다음과 같은 과정을 통해 이용할 수 있습니다:

1. 로그인(Google계정 연동)  
2. 전신 사진 1회 업로드  
3. 마음에 드는 중고 의류에서 **Try on now** 클릭  
4. 서버가 AI 모델을 통해 가상 착용 이미지를 생성  
5. 팝업으로 결과 이미지를 제공

## 🛠 2. 기술 스택

### **Frontend**
- HTML5
- CSS3
- JavaScript 

### **Backend**
- Flask 
- Google Gemini API (Nanobanana)
- Render Deployment (Server) 
- Supabase Python SDK  

---

## 🏗 3. 시스템 아키텍처

```text
[Client] 
   ↓  (Google Login via Supabase OAuth)
[Supabase Auth]
   ↓ user_id
[Client]
   ↓  (file upload)
[Backend API] → Supabase Storage
   ↓
(VTON AI Model) -> now using NanoBanana
   ↓
[Client Popup Result]
```

## 💻 4.실행방법
## Setup
**환경설정**: 아래의 KEY들이 포함된 `.env` 파일을 `backend/` 디렉토리에 추가하세요.
- `OPENAI_API_KEY` - OpenAI API access
- `GOOGLE_API_KEY` - Google ai API access
- `SUPABASE_KEY` - Supabase database access

```
backend/
├── app.py
├── nanobanana.py 
├── .env    # You need to create .env file with api keys
└── requirements.txt                
```
Vcloset은 Render를 통해 백엔드서버가 호스팅 되지만, 직접 돌리기를 희망할 경우 아래의 명령어를 따라주세요.
```bash
git clone https://github.com/TaeHoseong/Vcloset.git
cd backend
pip install -r requirements.txt
```
백엔드 서버를 실행하기 위해서는 아래 명령어를 실행한 후 api url을 `index.html`에 수정해주시면 됩니다. 
```bash
gunicorn app:app # 또는
python3 app.py
```
마침내! Vcloset을 직접 실행시켜볼 수 있게됐습니다!  

++추가로, Virtual Try On 기능만 따로 실행해보고 싶으시다면 `nanobanana.py`를 실행시키면 됩니다.
```bash
python3 nanobanana.py --person="person_img_path" --garment="garment_img_path"
```

