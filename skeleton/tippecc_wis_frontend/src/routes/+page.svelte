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
	  console.log( data)
	  climateFunctions = convertToClimateFunctionObjects(data)
	  console.log (climateFunctions)
    }

	function convertToClimateFunctionObjects(jsonArray: { id: number; name: string}[]): ClimateFunction[] {
    	return jsonArray.map(obj => new ClimateFunction(obj.id, obj.name));
	}

	//climateFunctions = [{id: 1,name: "t1"},{id: 2,name: "t2"}]
	//
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
						<ClimateFunctionCard climateFunction = {climateFunction}/>
					{/each}
				{/if} 
			</div>
		<p>test</p>
		</div>
	</div>
</div>
