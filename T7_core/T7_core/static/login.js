console.log('Hola mundo')

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const video = document.getElementById('video-element')
const image = document.getElementById('img-element')
const captureBtn = document.getElementById('capture-btn')
const reloadBtn = document.getElementById('reload-btn')

reloadBtn.addEventListener('click', () => {
    window.location.reload()
})

// Verifica si la API getUserMedia está disponible
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            console.log("Cámara encendida");
            console.log(stream.getTracks()[0].getSettings());
            const { height, width} = stream.getTracks()[0].getSettings();
            video.play(); // Asegúrate de reproducir el video
            captureBtn.addEventListener('click', () => {
                captureBtn.classList.add('not-visible');
                const track = stream.getVideoTracks()[0];
                const imageCapture = new imageCapture(track);
                video.play();
                console.log(imageCapture);
                imageCapture.takePhoto()
                    .then(blob => {
                        console.log("Foto tomada: ", blob);
                        const img = new Image(width, height);
                        img.src = URL.createObjectURL(blob);
                        image.append(img);

                        video.classList.add('not-visible');
                        const reader = new FileReader(blob);
                        reader.readAsDataURL(blob);
                        reader.onloadend = () => {
                            const base64String = reader.result;
                            console.log(base64String);
                            const fd = new FormData();
                            fd.append('csrftoken', csrftoken);
                            fd.append('photo', base64String);
                            $.ajax({
                                type: 'POST',
                                url: '/classify/',
                                enctype: 'multipart/form-data',
                                data: fd,
                                processData: false,
                                contentType: false,
                                success: function(response){
                                    console.log(response);
                                    window.location.href = window.location.origin;
                                },
                                error: function(error){
                                    console.error(error);
                                }
                            });
                        }
                    })
                    .catch(error => console.error("Error al tomar la foto: ", error));

            });
        })
        .catch((error) => {
            console.error("Error al acceder a la cámara: ", error);
        });
} else {
    console.error("La API getUserMedia no está soportada en este navegador.");
}
