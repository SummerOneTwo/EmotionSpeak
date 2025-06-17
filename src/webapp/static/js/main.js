// EmotionSpeak 前端主要JavaScript文件

// 等待 DOM 加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const elements = {
        textInput: document.getElementById('text-input'),
        analyzeBtn: document.getElementById('analyze-btn'),
        ttsBtn: document.getElementById('tts-btn'),
        wordcloudBtn: document.getElementById('wordcloud-btn'),
        clearBtn: document.getElementById('clear-btn'),
        pasteBtn: document.getElementById('paste-btn'),
        resultContainer: document.getElementById('result-container'),
        loadingIndicator: document.getElementById('loading'),
        audioPlayer: document.getElementById('audio-player'),
        downloadAudioBtn: document.getElementById('download-audio'),
        shareAudioBtn: document.getElementById('share-audio'),
        tabButtons: document.querySelectorAll('.tab-btn'),
        tabPanes: document.querySelectorAll('.tab-pane'),
        emotionsChart: document.getElementById('emotions-chart'),
        wordcloudContainer: document.getElementById('wordcloud-container')
    };

    // 初始化图表实例
    let charts = {
        emotions: null,
        wordcloud: null
    };

    // 情感名称映射
    const emotionNames = {
        joy: '喜悦',
        sadness: '悲伤',
        anger: '愤怒',
        fear: '恐惧',
        surprise: '惊讶',
        disgust: '厌恶',
        neutral: '中性'
    };

    // 标签页切换
    elements.tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            
            // 更新按钮状态
            elements.tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // 更新内容显示
            elements.tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === `${tabId}-tab`) {
                    pane.classList.add('active');
                }
            });

            // 调整图表大小
            if (tabId === 'emotions' && charts.emotions) {
                charts.emotions.resize();
            } else if (tabId === 'wordcloud' && charts.wordcloud) {
                charts.wordcloud.resize();
            }
        });
    });

    // 清空文本
    elements.clearBtn.addEventListener('click', () => {
        elements.textInput.value = '';
        elements.textInput.focus();
    });

    // 粘贴文本
    elements.pasteBtn.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            elements.textInput.value = text;
        } catch (err) {
            showError('无法访问剪贴板，请手动粘贴文本');
        }
    });

    // 分析按钮点击事件
    elements.analyzeBtn.addEventListener('click', async function() {
        const text = elements.textInput.value.trim();
        
        if (!text) {
            showError('请输入要分析的文本');
            return;
        }
        
        try {
            showLoading();
            
            // 发送分析请求
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || '分析失败');
            }
            
            // 显示分析结果
            displayResults(data);
            
            // 更新情感分布图表
            updateEmotionsChart(data.emotion.emotion_scores);
            
            // 更新词云图
            updateWordcloud(data.context.keywords);
            
        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    // 显示分析结果
    function displayResults(data) {
        const { emotion, intensity, context, voice } = data;
        
        // 创建结果HTML
        let html = `
            <div class="main-sentiment">
                <div class="dominant-emotion">
                    <h3>主导情感: ${getEmotionName(emotion.dominant_emotion)}</h3>
                    <div class="confidence-score">置信度: ${(emotion.confidence * 100).toFixed(1)}%</div>
                    <div class="sentiment-score">情感得分: ${(emotion.sentiment_score * 100).toFixed(1)}%</div>
                </div>
            </div>
            
            <div class="emotion-dimensions">
                <h3>情感维度分析</h3>
                <div class="emotion-grid">
                    ${Object.entries(emotion.emotion_scores)
                        .sort((a, b) => b[1] - a[1])
                        .map(([emotion, score]) => `
                            <div class="emotion-item">
                                <div class="emotion-label">
                                    <span>${getEmotionName(emotion)}</span>
                                    <span>${(score * 100).toFixed(1)}%</span>
                                </div>
                                <div class="emotion-progress">
                                    <div class="emotion-fill" style="width: ${score * 100}%"></div>
                                </div>
                            </div>
                        `).join('')}
                </div>
            </div>
            
            <div class="intensity-section">
                <h3>情感强度</h3>
                <div class="intensity-info">
                    <p>强度级别: ${intensity.intensity_level}</p>
                    <p>强度得分: ${(intensity.intensity_score * 100).toFixed(1)}%</p>
                </div>
            </div>
            
            <div class="context-section">
                <h3>上下文分析</h3>
                <div class="context-info">
                    <p>语境类型: ${context.context_type}</p>
                    <div class="keyword-tags">
                        ${context.keywords.map(keyword => `
                            <span class="keyword-tag">${keyword.text}</span>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="voice-section">
                <h3>语音参数</h3>
                <div class="voice-params">
                    <p>音调: ${voice.pitch.toFixed(2)}</p>
                    <p>语速: ${voice.speed.toFixed(2)}</p>
                    <p>音量: ${voice.volume.toFixed(2)}</p>
                    <p>风格: ${voice.style}</p>
                </div>
            </div>
        `;
        
        elements.resultContainer.innerHTML = html;
        elements.resultContainer.style.display = 'block';
    }

    // 更新情感分布图表
    function updateEmotionsChart(emotions) {
        if (!charts.emotions) {
            charts.emotions = echarts.init(elements.emotionsChart);
        }
        
        const option = {
            title: {
                text: '情感分布',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c}%'
            },
            series: [{
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '20',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: Object.entries(emotions).map(([name, value]) => ({
                    name: getEmotionName(name),
                    value: (value * 100).toFixed(1)
                }))
            }]
        };
        
        charts.emotions.setOption(option);
    }

    // 更新词云图
    function updateWordcloud(keywords) {
        if (charts.wordcloud) {
            charts.wordcloud.dispose();
        }
        
        const words = keywords.map((keyword, index) => [
            keyword.text,
            Math.max(10, 100 - index * 5)
        ]);
        
        charts.wordcloud = WordCloud(elements.wordcloudContainer, {
            list: words,
            gridSize: 16,
            weightFactor: 10,
            fontFamily: 'Microsoft YaHei',
            color: function(word, weight) {
                return `rgb(${Math.floor(Math.random() * 100 + 100)}, ${Math.floor(Math.random() * 100 + 100)}, ${Math.floor(Math.random() * 100 + 100)})`;
            },
            hover: window.drawBox,
            click: function(item) {
                console.log(item[0], item[1]);
            }
        });
    }

    // 语音合成按钮事件
    elements.ttsBtn.addEventListener('click', async function() {
        const text = elements.textInput.value.trim();
        
        if (!text) {
            showError('请输入要合成语音的文本');
            return;
        }
        
        try {
            showLoading();
            
            const response = await fetch('/tts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    text: text,
                    auto_analyze: true 
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || '语音合成失败');
            }
            
            // 播放音频
            elements.audioPlayer.src = data.audio_url;
            elements.audioPlayer.play();
            
        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    // 下载音频
    elements.downloadAudioBtn.addEventListener('click', () => {
        if (elements.audioPlayer.src) {
            const link = document.createElement('a');
            link.href = elements.audioPlayer.src;
            link.download = 'emotion_speech.mp3';
            link.click();
        } else {
            showError('没有可下载的音频');
        }
    });

    // 分享音频
    elements.shareAudioBtn.addEventListener('click', async () => {
        if (!elements.audioPlayer.src) {
            showError('没有可分享的音频');
            return;
        }
        
        try {
            if (navigator.share) {
                await navigator.share({
                    title: 'EmotionSpeak 语音',
                    text: '听听这段情感语音',
                    url: elements.audioPlayer.src
                });
            } else {
                // 复制链接到剪贴板
                await navigator.clipboard.writeText(elements.audioPlayer.src);
                showSuccess('音频链接已复制到剪贴板');
            }
        } catch (err) {
            showError('分享失败');
        }
    });

    // 工具函数
    function getEmotionName(emotion) {
        return emotionNames[emotion] || emotion;
    }

    function showLoading() {
        elements.loadingIndicator.classList.add('active');
    }

    function hideLoading() {
        elements.loadingIndicator.classList.remove('active');
    }

    function showError(message) {
        alert(message);
    }

    function showSuccess(message) {
        alert(message);
    }

    // 窗口大小改变时调整图表大小
    window.addEventListener('resize', () => {
        if (charts.emotions) {
            charts.emotions.resize();
        }
        if (charts.wordcloud) {
            charts.wordcloud.resize();
        }
    });
});