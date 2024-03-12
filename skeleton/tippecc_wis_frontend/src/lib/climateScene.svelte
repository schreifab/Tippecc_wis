<!--Component for the definition of the aoi
	Can be defined via a map or input forms

-->
<script lang="ts">
	//Funtions for writing aoi as variable in vars.ts
	//this makes the variable avialable in other components
	import { aoi } from '$lib/vars';
	import { updateAoi } from '$lib/vars';
	let aoiInput = aoi;
	$: updateAoi(aoiInput);

	//import
	import { onMount } from 'svelte';
	import Map from 'ol/Map';
	import View from 'ol/View';
	import TileLayer from 'ol/layer/Tile';
	import OSM from 'ol/source/OSM';
	import ExtentInteraction from 'ol/interaction/Extent.js';
	import { shiftKeyOnly } from 'ol/events/condition.js';
	import { transformExtent } from 'ol/proj';

	/**
	 * @type {Map}
	 */
	let map: Map;
	/**
	 * @type {import("ol/interaction/Interaction").default}
	 */
	let extent: ExtentInteraction;
	/**
	 * @type {any[]}
	 */
	let minx: number;

	let map_exists: boolean = false;
	// Initialize the map when the component is mounted
	onMount(initializeMap);
	function initializeMap() {
		if (map_exists === false) {
			//target the map container in html section
			map = new Map({
				target: 'map-container',
				layers: [
					new TileLayer({
						source: new OSM()
					})
				],
				//set map view/ extent that is displayed
				view: new View({
					center: [0, 0],
					zoom: 2,
					extent: [75030.694516244, -4411300.315555968, 6438618.6747234445, 1202883.092131822] // adjust to real extent + x?
				})
			});

			extent = new ExtentInteraction({ condition: shiftKeyOnly });
			map.addInteraction(extent);
			map_exists = true;

			extent.on('extentchanged', function () {
				// [minx, miny, maxx, maxy]
				// transform extent form mercator to wsgi
				var lon_lat_extent = transformExtent(extent.getExtent(), 'EPSG:3857', 'EPSG:4326');
				// Save and round extent n variable
				// Because of binding the Variable is alos displayed in the forms
				aoiInput[0] = Number(lon_lat_extent[1].toFixed(3));
				aoiInput[1] = Number(lon_lat_extent[3].toFixed(3));
				aoiInput[2] = Number(lon_lat_extent[0].toFixed(3));
				aoiInput[3] = Number(lon_lat_extent[2].toFixed(3));
			});
		}
	}
</script>
<!--forms
variables are bound to aoi in vars.ts
-->
<div class="card">
	<div class="card-body pb-3 pl-3 pr-3 pt-2">
		<div class="card p-2 variant-filled-surface">Area of Interest</div>
		<label class="label">
			Lat (min): <input
				class="input"
				type="number"
				step="0.001"
				placeholder="lat-min"
				bind:value={aoiInput[0]}
			/>
			Lat (max):
			<input
				class="input"
				type="number"
				step="0.001"
				placeholder="lat-max"
				bind:value={aoiInput[1]}
			/>
			Lon (min):
			<input
				class="input"
				type="number"
				step="0.001"
				placeholder="lon-min"
				bind:value={aoiInput[2]}
			/>
			Lon (max):
			<input
				class="input"
				type="number"
				step="0.001"
				placeholder="lon-max"
				bind:value={aoiInput[3]}
			/>
		</label>
	</div>
</div>
<div>
	Use Shift+Drag to draw an extent. Shift+Drag on the corners or edges of the extent to resize it.
	Shift+Click off the extent to remove it.
</div>
<!--map container here-->
<div class="map" id="map-container" />

<style>
	@import '/node_modules/ol/ol.css';
	.map {
		width: 100%;
		height: 400px;
	}
</style>
