const APP_ID = "3a380ab62bca44a5a942390bdad2f272"

let uid= sessionStorage.getItem('uid')

if(!uid){
    uid=String(Math.floor(Math.random() * 10000))
    sessionStorage.setItem('uid',uid)
}

// alert(uid)

let token=null;
let client;

const  queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
let roomId = urlParams.get('room')

if(!roomId){
    roomId='main'
}

let localTrack = []
let remoteUsers = {}

let joinRoomInit = async () =>
{
    client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})
    try {
        await client.join(APP_ID, roomId, token, uid);
        joinStream();
    } catch (error) {
        console.error("Error joining Agora room:", error);
    }
}

let joinStream = async () =>
{
    localTrack = await AgoraRTC.createMicrophoneAndCameraTracks()
    await client.publish(localTrack[0],localTrack[1])
    let player = `
        <div class='video__container' id='user-container-${uid}'>
            <div className='video-player' id='user-${uid}'>
                 </div>
        </div>`
    document.getElementById('streams__container').insertAdjacentHTML('beforeend', player);

    localTrack[1].play(`user-${uid}`);
    console.log(localTrack)
    // await client.publish(localTrack[0],localTrack[1])

    // localTrack[1].play(`user-${uid}`).catch((error) => {
    //     console.error("Error playing local video track:", error);
    // });
}
joinRoomInit()