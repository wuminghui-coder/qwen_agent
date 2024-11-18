function isEmpty(value) {
    return !value || value.trim().length === 0;
}

function generateRandomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }
    return result;
}


function addMessage(message, className, icon) {
    const chatBox = document.getElementById('chat-box-message');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);

    const img = document.createElement('img');
    img.src = icon;
    img.classList.add('icon');

    const textElement = document.createElement('div');
    textElement.classList.add('message-content', className === 'user-message' ? 'user-content' : 'bot-content');
    textElement.textContent = message;

    messageElement.appendChild(img);
    messageElement.appendChild(textElement);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到最新消息
}

function addSongList(message, play_list, className, icon)
{
    const chatBox = document.getElementById('chat-box-message');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);

    const img = document.createElement('img');
    img.src = icon;
    img.classList.add('icon');

    const textElement = document.createElement('div');
    textElement.classList.add('message-content', className === 'user-message' ? 'user-content' : 'bot-content');
    textElement.textContent = message; // 机器人的文本回复

    messageElement.appendChild(img);
    messageElement.appendChild(textElement);

    for (let i = 0; i < play_list.length; i++) {
        const image_info = play_list[i];
        const songContainer = document.createElement('div');
        songContainer.classList.add('song-info');
    
        const songImage = document.createElement('img');
        const image_url = image_info.hasOwnProperty("image");
        songImage.src = image_info.image || "https://p2.music.126.net/o_OjL_NZNoeog9fIjBXAyw==/18782957139233959.jpg";
       

        songImage.classList.add('song-image');
    
        const songTitle = document.createElement('span');
        songTitle.textContent = image_info.song_name;
    
        // 添加点击事件监听器
        songContainer.addEventListener('click', () => {
            if (image_info.song_url == null)
            {
                fetchData('http://172.30.13.160:5001/song/' + image_info.song_id).then(data => {
                    if (data) {
                        const image_url = "url(" + data["slots"][0]["image"] + ")";
                        document.documentElement.style.setProperty('--alarm-bg', image_url);
                        play_music(data["slots"][0]["lyric"], data["slots"][0]["artist"], data["slots"][0]["song_name"], data["slots"][0]["song_url"])
                    } else {
                        console.log('未能获取到数据');
                    }
                });
            } else {
                const image_url = "url(" + image_info["image"] + ")";
                document.documentElement.style.setProperty('--alarm-bg', image_url);
                play_music(image_info["lyric"], image_info["artist"], image_info["song_name"], image_info["song_url"])
            }
        });

        songContainer.appendChild(songImage);
        songContainer.appendChild(songTitle);
        messageElement.appendChild(songContainer);
    }

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到最新消息
}

function addSongMessage(message, song_name, image, className, icon) {
    const chatBox = document.getElementById('chat-box-message');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);

    const img = document.createElement('img');
    img.src = icon;
    img.classList.add('icon');

    const songContainer = document.createElement('div');
    songContainer.classList.add('song-info');

    const songImage = document.createElement('img');
    songImage.src = image;
    songImage.classList.add('song-image');

    const songTitle = document.createElement('span');
    songTitle.textContent = song_name;

    songContainer.appendChild(songImage);
    songContainer.appendChild(songTitle);

    const textElement = document.createElement('div');
    textElement.classList.add('message-content', className === 'user-message' ? 'user-content' : 'bot-content');
    textElement.textContent = message; // 机器人的文本回复

    messageElement.appendChild(img);
    messageElement.appendChild(textElement);
    messageElement.appendChild(songContainer);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到最新消息
}

function  addRobotMessage(message, className, icon)
{
    const chatBox = document.getElementById('chat-box-message');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);

    const img = document.createElement('img');
    img.src = icon;
    img.classList.add('icon');

    const textElement = document.createElement('div');
    textElement.classList.add('message-content', className === 'user-message' ? 'user-content' : 'bot-content');
    textElement.textContent = message; // 机器人的文本回复

    messageElement.appendChild(img);
    messageElement.appendChild(textElement);
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 自动滚动到最新消息
}


function play_buton()
{
    let playBut = document.getElementById("play");//播放按钮
    let myAudio = document.getElementById("myAudio");//播放器
    let controlDom = document.getElementById('control');//控件

    playBut.addEventListener("click", playF);//点击事件
    function playF() {
        //判断当前是否在播放
        let flag = Array.from(controlDom.classList).some(function (item) {
            return item == "active";
        });
        if (flag) {
            //播放中点击暂停
            controlDom.classList.remove('active');
            myAudio.pause();
        } else {
            controlDom.classList.add('active');
            myAudio.play();
        }
    }
}

play_buton() //按键初始化

function play_music(lyric, artist, song_name, url){
    var lyric_data = ""
    if (lyric == null) {
        lyric_data = ""
    } 

    const songName = document.getElementById('song_name');
    if (songName.firstChild)
    {
        songName.removeChild(songName.firstChild);
        songName.textContent = song_name + "  ";
        const span = document.createElement('span');
        span.className = 'name';
        span.textContent = artist;
        songName.appendChild(span);
    }

    //播放器
    let myAudio = document.getElementById("myAudio");
    let controlDom = document.getElementById('control');//控件
    const audioSource = document.getElementById('audio_id');
    let lrc_box = document.querySelector('.lrc-box')
    if (lrc_box.firstChild)
    {
        while (lrc_box.firstChild)
            lrc_box.removeChild(lrc_box.firstChild);
    }

    myAudio.removeEventListener('timeupdate', setLrc);

    audioSource.src = url;
    myAudio.load(); // 重新加载音频

    // 获取时间和歌词
    function getLrcObj(str) {
        const arr = str.split(']');
        return {
            time: formateTime(arr[0].substring(1)),
            word: arr[1],
        };
    }

    // 把时间转化成秒
    function formateTime(str) {
        const arr = str.split(':');
        return +arr[0] * 60 + +arr[1];
    }

    function getLrc(str) {
        const strArr = str.split('\n');
        let arr = [];
        for (let i = 0; i < strArr.length; i++) {
            let obj = getLrcObj(strArr[i]);
            arr.push(obj);
        }
        return arr;
    }

    //显示歌词
    let lrcArr = [];
    function showLrc() {
        const fragment = document.createDocumentFragment();
        lrcArr = getLrc(lyric_data);
        for (let i = 0; i < lrcArr.length; i++) {
            li = document.createElement('li');
            li.textContent = lrcArr[i].word;//歌词
            fragment.appendChild(li);
        }
        lrc_box.appendChild(fragment);
    }

    showLrc();

    // 获取当前播放的歌词下标
    function getArrIndex() {
        const currentTime = myAudio.currentTime;
        let index = lrcArr.findIndex(function (item) {
            return item.time > currentTime
        })
        if (index == -1) {
            return lrcArr.length - 1;
        }
        return index - 1;
    }

    //滚动区域高度
    let ulDom = document.querySelector(".container ul");
    const containerH = document.querySelector(".container").clientHeight;
    //最大移动高度
    const maxOffset = ulDom.clientHeight - containerH;

    //实时获取歌曲播放进度
    function setLrc() {
        setProgress();//设置进度条
        const nowIndex = getArrIndex();
        const allLiHeight = nowIndex * 30;
        const half = containerH / 2; // 容器的一半高度
        // 移动多少
        let offset = allLiHeight + 30 / 2 - half;
        if (offset < 0) {
            offset = 0;
        }
        if (offset > maxOffset) {
            offset = maxOffset;
        }

        //滚动歌词
        ulDom.style.transform = `translateY(-${offset}px)`;

        let li = document.querySelector('.on');
        if (li) {
            li.classList.remove('on');
        }
        //设置 当前歌词高亮
        li = ulDom.children[nowIndex];

        if (li) {
            li.classList.add('on');
        }
    }
    // 监听播放进度
    myAudio.addEventListener('timeupdate', setLrc);

    // 设置进度条
    const slider = document.getElementById('myRange');
    const progress = document.getElementById('progress');

    //进度提拖动
    slider.oninput = function () {
        progress.style.width = `${this.value}%`;
        // 获取音乐总时长，单位是秒
        let duration = myAudio.duration;
        //修改当前播放时间
        myAudio.currentTime = this.value / 100 * duration;
    }

    //设置进度条
    function setProgress() {
        let duration = myAudio.duration;
        const currentTime = myAudio.currentTime;
        let val = parseInt(currentTime / duration * 100);
        //设置进度提值 
        slider.value = val;
        progress.style.width = `${val}%`;
    }
    controlDom.classList.add('active');
    myAudio.play();
}

var globalUser  = '';
var globalConId ='';


async function fetchData(url) {
    try {
        // 发送 GET 请求
        const response = await fetch(url);
        
        // 检查响应是否为成功状态
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // 解析 JSON 数据
        const data = await response.json();
        
        // 返回获取到的数据
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null; // 或者返回一个错误消息
    }
}

function sendRequest(send_data){
    const cachedData = localStorage.getItem("user");
    if (cachedData) {
        globalUser = cachedData;
    } else {
        globalUser = generateRandomString(10);
        localStorage.setItem("user", globalUser);
    }

    let postData = {
        query: send_data,
        user:  globalUser,
    };

    if (!isEmpty(globalConId))
    {
        postData["conversation_id"] = globalConId;
    }

    fetch('http://172.30.13.160:5001/v4/chat-messages', {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',
                'authorization':'app-AvhB6c5obuZhgzt3gnXedMlz'
        },
        body: JSON.stringify(postData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('网络响应不是 OK');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        const songList= data.hasOwnProperty("slots");

        if (data["slots"] != null 
            && songList 
            && data["slots"].length >= 1 
            && data?.slots?.[0]?.song_url)
        {
            if (data?.slots?.[0]?.image) {
                const image_url = "url(" + data["slots"][0]["image"] + ")";
                document.documentElement.style.setProperty('--alarm-bg', image_url);
            }

            if (data?.slots?.[0]?.song_name && data?.slots?.[0]?.song_url)
            {
                play_music(data["slots"][0]["lyric"], data["slots"][0]["artist"], data["slots"][0]["song_name"], data["slots"][0]["song_url"])
                addSongList(data.message, data["slots"], 'bot-message', "https://cdn.baseus.cn/admin/other/Yzm5eeFbxL7uCK0jqRYZdZvFrIKmtKwU.png");
            }
        } else {
            addRobotMessage(data.message, 'bot-message', "https://cdn.baseus.cn/admin/other/Yzm5eeFbxL7uCK0jqRYZdZvFrIKmtKwU.png");
        }
    
        globalConId = '';
        globalConId = data["conversation_id"];
        showMessage(data.message, 20000);
    })
    .catch(error => {
        //document.getElementById('responseContainer').innerText = error.message;
    });
}

function registration_button(){
    const input = document.querySelector('.text-input');
    const icon_id = document.getElementById('icon_id');

    addRobotMessage("我是倍小狮，我可以帮你查歌曲，有什么不懂得问题可以询问我哦", 'bot-message', "https://cdn.baseus.cn/admin/other/Yzm5eeFbxL7uCK0jqRYZdZvFrIKmtKwU.png");
    
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            addMessage(input.value, 'user-message', "https://cdn.baseus.cn/admin/other/Yzm5eeFbxL7uCK0jqRYZdZvFrIKmtKwU.png"); // 用户图标
            sendRequest(input.value)
            input.value = ''; // 清空输入框
        }
    });
    
    icon_id.addEventListener('click', function() { 
        if (input.value.trim() !== '') {
            addMessage(input.value, 'user-message', "https://cdn.baseus.cn/admin/other/Yzm5eeFbxL7uCK0jqRYZdZvFrIKmtKwU.png"); // 用户图标
            sendRequest(input.value)
            input.value = ''; // 清空输入框
        }
    });
}

registration_button();