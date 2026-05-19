const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;

// JSON 및 정적 파일(HTML) 미들웨어 세팅
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// 프론트엔드가 보낸 질문을 FastAPI(8000번)로 중계하는 라우터
// server.js 내부의 app.post('/api/chat', ...) 라우터 부분 수정
app.post('/api/chat', async (req, res) => {
    try {
        const userQuestion = req.body.question;
        
        // 🌟 톰캣 포트인 8181번과 프로젝트 컨텍스트 패스(/rag_backend)를 명시해 줍니다!
        const response = await axios.post('http://localhost:8181/rag_backend/api/chat', {
            question: userQuestion
        });
        
        res.json(response.data);
    } catch (error) {
        console.error("Spring Framework 연동 에러:", error.message);
        res.status(500).json({ error: "스프링 백엔드 서버와 통신 중 오류가 발생했습니다." });
    }
});

app.listen(PORT, () => {
    console.log(`Express Web Server가 http://localhost:${PORT} 에서 구동 중입니다.`);
});