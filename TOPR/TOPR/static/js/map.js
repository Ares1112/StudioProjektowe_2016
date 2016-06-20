
var last_layer;
function reloadLayer(map) {

	var tourists = new ol.layer.Vector({
		source: new ol.source.Vector({
			url: '{% url 'api_get_tourists' %}',
			format: new ol.format.KML()
		})
	});
	map.removeLayer(last_layer);
	last_layer = tourists;
	map.addLayer(tourists);
}

var projection = ol.proj.get('EPSG:3857');

var raster = new ol.layer.Tile({
	source: new ol.source.BingMaps({
		imagerySet: 'AerialWithLabels',
		key: 'AkGbxXx6tDWf1swIhPJyoAVp06H0s0gDTYslNWWHZ6RoPqMpB9ld5FY1WutX8UoF'
	})
});

var vector = new ol.layer.Vector({
	source: new ol.source.Vector({
		url: '{% url 'api_get_routes' %}',
		format: new ol.format.KML()
	})
});


var map = new ol.Map({
	layers: [raster, vector],
	target: document.getElementById('map'),
	view: new ol.View({
		center: [2176668.590591357, 6377294.143888826],
		projection: projection,
		zoom: 13
	})
});
window.setInterval(reloadLayer, 5000, map);
