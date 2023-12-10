<script lang="ts">
	import ClimateFunctionCard from "$lib/climateFunctionCard.svelte";
	import {onMount} from 'svelte'
	import {ClimateFunction} from "../ClimateFunction"
	//let climateFunctions = []
    let climateFunctions:  ClimateFunction[] = [];
	// Fetch data for the climate indices functions from the Django API
    async function fetchClimateFunctions() {
      const response = await fetch('http://localhost:8000/api/climate-indices/');
      const data = await response.json();
	  climateFunctions = convertToClimateFunctionObjects(data)
    }

	function convertToClimateFunctionObjects(jsonArray: { id: number; name: string, description: string}[]): ClimateFunction[] {
    	return jsonArray.map(obj => new ClimateFunction(obj.id, obj.name, obj.description));
	}

	function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		const id = event.detail.id;
		console.log('Benutzerdefiniertes Ereignis aus OtherComponent. ID:', id);
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
		<p>test</p>
		</div>
	</div>
</div>