var myArray = [];
var siderealtime = -1;
$.getJSON('/siderealtime', function(jd) {
  siderealtime = jd.siderealtime;
});
$.getJSON('/safezone', function(jd) {
  $.each(jd.safeZone, function(i, obj) {
    jd.safeZone[i][0]+=siderealtime;
    /*if (jd.safeZone[i][0] < 0) {
      jd.safeZone[i][0] = 365 - jd.safeZone[i][0];
    }*/
    myArray.push(jd.safeZone[i]);
  });
});




var aladin = A.aladin('#aladin-lite-div', {target: 'M 31', fov: 60});

var overlay = A.graphicOverlay({color: '#ee2345', lineWidth: 3});
aladin.addOverlay(overlay);
//overlay.addFootprints([A.polygon(myArray)]);
overlay.add(A.polyline(myArray));
aladin.addCatalog(A.catalogFromVizieR('VII/118', 'M 1', 150, {onClick: 'showTable'}));
