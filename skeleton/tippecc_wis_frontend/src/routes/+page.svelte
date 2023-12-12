<script lang="ts">
	//imports
	import ClimateFunctionCard from "$lib/climateFunctionCard.svelte";
	import {onMount} from 'svelte'
	import {ClimateFunction} from "../ClimateFunction"
	import type{FunctionDetails} from "$lib/interfaces"
	import FunctionDetailsCard from "$lib/functionDetailsCard.svelte";

	//let climateFunctions = []
    let climateFunctions:  ClimateFunction[] = [];
	let booleanFunctionSelected: Boolean = false;
	let functionDetails: FunctionDetails

	// Fetch data for the climate indices functions from the Django API
    async function fetchClimateFunctions() {
      const response = await fetch('http://localhost:8000/api/climate-indices/');
      const data = await response.json();
	  climateFunctions = convertToClimateFunctionObjects(data)
    }

	async function fetchFunctionDetails(id: number) {
    try {
        const response = await fetch('http://localhost:8000/api/climate-indices/'.concat(id.toString()));
        const data = await response.json();
		functionDetails = data as FunctionDetails

		
    } catch (error) {
        // error handling
        console.error('Fehler beim Abrufen der Daten:', error);
        throw new Error('Fehler beim Abrufen der Daten');
    }
	}


	function convertToClimateFunctionObjects(jsonArray: { id: number; name: string, description: string}[]): ClimateFunction[] {
    	return jsonArray.map(obj => new ClimateFunction(obj.id, obj.name, obj.description));
	}

	function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		const id = event.detail.id;
		fetchFunctionDetails(id);
		booleanFunctionSelected = true;
		
	}

    // Call the fetchClimateIndices function when the component is mounted
    onMount(() => {
      fetchClimateFunctions();
	  
    });

	
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-5">
		<div class="grid h-screen grid-cols-2 gap-5">
			<div>				
				{#if climateFunctions.length === 0}
					<p>Loading...</p>
				{:else} 
					{#each climateFunctions as climateFunction}
						<ClimateFunctionCard climateFunction = {climateFunction} on:functionSelected={handleFunctionSelected}/>
					{/each}
				{/if} 
			</div>
			<div>
				{#if functionDetails !== undefined}
					<FunctionDetailsCard functionDetails = {functionDetails}/>
				{/if}
			</div>
		</div>
	</div>
</div>
