
//<script src="test.js" type="text/javascript"></script>
function initialize() {
    var options = {atmosphere: true, center: [0, 0], zoom: 0, sky: true, zooming: true,  unconstrainedRotation: true};
    var earth = new WE.map('earth_div', options);

    WE.tileLayer('http://tileserver.maptiler.com/nasa/{z}/{x}/{y}.jpg', {
        minZoom: 0,
        maxZoom: 5,
        attribution: 'NASA',
    }).addTo(earth);

    var marker = WE.marker([51.5, -0.09]).addTo(earth);
    marker.bindPopup("Disease Outbreak for some disease.", {maxWidth: 120, maxHeight: 300,  closeButton: true}).openPopup();

    var marker2 = WE.marker([30.058056, 31.228889]).addTo(earth);
    marker2.bindPopup("Maybe California!", {maxWidth: 120, closeButton: true}).openPopup();

    var markerCustom = WE.marker([50, -9], '/img/logo-webglearth-white-100.png', 100, 24).addTo(earth);
}
function flyTo() {
    earth.fitBounds([51.5, -0.09]);
    earth.panInsideBounds([[22, 122], [48, 154]],
            {heading: 90, tilt: 25, duration: 1});
}
function panTo(coords) {
    earth.panTo(coords);
}



function myFunction() {
    alert("MapOutbreaks, a team of software developers at UNSW in 2019, is an online platform in utilizing online informal sources for disease outbreak monitoring and real-time surveillance of emerging public health threats. The freely available Web site deliver real-time intelligence on a broad range of emerging infectious diseases for a diverse audience including libraries, local health departments, governments, and international travelers. MapOutbreaks brings together disparate data sources, including online news aggregators and validated official reports, to achieve a unified and comprehensive view of the current global state of infectious diseases and their effect on human and animal health. Through an automated process, updating 24/7/365, the system monitors, organizes, integrates, filters, visualizes and disseminates online information about emerging diseases in nine languages, facilitating early detection of global public health threats.")
}

function myFunctionContactUs() {
    alert("Send your queries to mapOutbreak@gmail.com");
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function myFunctionNews() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
