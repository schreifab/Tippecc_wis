<script lang="ts">
    import type { CreateQueryResult, QueryKey } from "@tanstack/svelte-query";
	import type { AxiosResponse, AxiosError } from "axios";

	import type { ClimateFunctionDetail } from "../model";   
    
    import { createApiClimateIndicesList, createApiClimateIndicesRetrieve } from "../api/api"
    import ClimateFunctionCard from "$lib/climateFunctionCard.svelte"
    import FunctionDetailsCard from "$lib/functionDetailsCard.svelte"
   	

    const climatefuncs = createApiClimateIndicesList()
    let idSelected: number = 0;
    $: funcDetails = createApiClimateIndicesRetrieve(idSelected);

    function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		idSelected = event.detail.id;
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
                    {/each}
                {/if} 
            </div>
            <div>
                {#if $funcDetails?.data?.data !== undefined}
                    <FunctionDetailsCard functionDetails = {$funcDetails.data.data}/>
                {/if}
            </div>
        </div>
    </div>
</div>
