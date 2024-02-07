<script lang="ts">
    import {aoi} from "$lib/vars"
    import {updateAoi} from "$lib/vars"
    let aoiInput = aoi
    $: updateAoi(aoiInput)

    import { onMount } from 'svelte';
    import Map from 'ol/Map';
    import View from 'ol/View';
    import TileLayer from 'ol/layer/Tile';
    import OSM from 'ol/source/OSM';
    import ExtentInteraction from 'ol/interaction/Extent.js';
    import { shiftKeyOnly } from 'ol/events/condition.js';

     /**
     * @type {Map}
     */
     let map;
    /**
     * @type {import("ol/interaction/Interaction").default}
     */
    let extent: ExtentInteraction;
    /**
     * @type {any[]}
     */
    let minx: number;
    // Initialize the map when the component is mounted
    onMount(initializeMap);
    function initializeMap() {
        map = new Map({
            target: 'map-container',
            layers: [
                new TileLayer({
                    source: new OSM()
                })
            ],
            view: new View({
                center: [0, 0],
                zoom: 2,
                extent: [75030.694516244, -4411300.315555968, 6438618.6747234445, 1202883.092131822] // adjust to real extent + x?
            })
        });
        extent = new ExtentInteraction({ condition: shiftKeyOnly });
        map.addInteraction(extent);
        extent.on('extentchanged', function () {
            // [minx, miny, maxx, maxy]
            console.log(extent.getExtent());
            minx = extent.getExtent()[0];
            aoiInput[0] = extent.getExtent()[0]
            aoiInput[1] = extent.getExtent()[2]
            aoiInput[2] = extent.getExtent()[1]
            aoiInput[3] = extent.getExtent()[3]
        });
    }
</script>
<div class = 'card'>
    <div class = 'card-body pb-3 pl-3' >
        aoi
        <label class="label">
            <input class="input" type="number" placeholder="lat-min" bind:value={aoiInput[0]}  />
            <input class="input" type="number" placeholder="lat-max" bind:value={aoiInput[1]}  />
            <input class="input" type="number" placeholder="lon-min" bind:value={aoiInput[2]}  />
            <input class="input" type="number" placeholder="lon-max" bind:value={aoiInput[3]}  />
        </label>
    </div>
</div>
<div>Top: {minx}</div>
<div>
    Use Shift+Drag to draw an extent. Shift+Drag on the corners or edges of the extent to resize it.
    Shift+Click off the extent to remove it.
</div>
<div>Example: https://openlayers.org/en/latest/examples/extent-interaction.html</div>
<div class="map" id="map-container" />
<style>
    @import '/node_modules/ol/ol.css';
    .map {
        width: 600px;
        height: 600px;
    }
</style>