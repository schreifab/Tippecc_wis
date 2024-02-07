<script lang="ts">
    import type { CreateQueryResult, QueryKey } from "@tanstack/svelte-query";
	import type { AxiosResponse, AxiosError } from "axios";

	import type { ClimateFunctionDetail } from "../model";   
    
    import { createApiClimateIndicesList, createApiClimateIndicesRetrieve } from "../api/api"
    import ClimateFunctionCard from "$lib/climateFunctionCard.svelte"
    import FunctionDetailsCard from "$lib/functionDetailsCard.svelte"
    import ClimateScene from "$lib/climateScene.svelte"
   	
    import { onMount } from 'svelte';
    import Map from 'ol/Map';
    import View from 'ol/View';
    import TileLayer from 'ol/layer/Tile';
    import OSM from 'ol/source/OSM';
    import ExtentInteraction from 'ol/interaction/Extent.js';
    import { shiftKeyOnly } from 'ol/events/condition.js';


    const climatefuncs = createApiClimateIndicesList()
    let idSelected: number = 0;
    $: funcDetails = createApiClimateIndicesRetrieve(idSelected);

    function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		idSelected = event.detail.id;
	}

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
    let minx;
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
        });
    }

</script>


<div class="container h-full mx-auto flex justify-center items-center">
    <div class="space-y-5">
        <div class="grid h-screen grid-cols-2 gap-5">
            <div>				
                {#if $climatefuncs.isLoading}
                    <p>Loading...</p>
                {:else if $climatefuncs.isError}
                    <span>Error: {$climatefuncs.error}</span>
                {:else} 
                    {#each $climatefuncs.data.data as climateFunction}
                        <ClimateFunctionCard climateFunction = {climateFunction} on:functionSelected={handleFunctionSelected}/>
                        <br>
                    {/each}
                {/if} 
                <ClimateScene />
            </div>
            <div>
                {#key $funcDetails}
                    {#if $funcDetails?.data?.data !== undefined}
                        <FunctionDetailsCard functionDetails = {$funcDetails.data.data}/>
                    {/if}
                {/key}
            </div>
        </div>
    </div>
</div>
