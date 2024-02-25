<script lang="ts">
	import type { CreateQueryResult, QueryKey } from '@tanstack/svelte-query';
	import type { AxiosResponse, AxiosError } from 'axios';

	import type { ClimateFunctionDetail } from '../model';

	import { createApiClimateIndicesList, createApiClimateIndicesRetrieve } from '../api/api';
	import ClimateFunctionCard from '$lib/climateFunctionCard.svelte';
	import FunctionDetailsCard from '$lib/functionDetailsCard.svelte';
	import ClimateScene from '$lib/climateScene.svelte';
	import DynamicOptions from './dynamicOptions.svelte';

	const climatefuncs = createApiClimateIndicesList();
	let idSelected: number = 0;
	$: funcDetails = createApiClimateIndicesRetrieve(idSelected);

	function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		idSelected = event.detail.id;
	}
</script>

<h2 class="text-center text-xl">TIPPECC climate indices web information system</h2>
<br />
<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-5">
		<div class="grid h-screen grid-cols-4 gap-5">
			<div>
				<ClimateScene />
			</div>
			<div>
				<DynamicOptions />
			</div>
			<div class="max-h-100 overflow-y-auto snap-y">
				<div class="grid gap-y-1">
					{#if $climatefuncs.isLoading}
						<p>Loading...</p>
					{:else if $climatefuncs.isError}
						<span>Error: {$climatefuncs.error}</span>
					{:else}
						{#each $climatefuncs.data.data as climateFunction}
							<div>
								<ClimateFunctionCard
									{climateFunction}
									on:functionSelected={handleFunctionSelected}
								/>
							</div>
						{/each}
					{/if}
				</div>
			</div>

			<div>
				{#key idSelected}
					{#if $funcDetails?.data?.data !== undefined}
						<FunctionDetailsCard functionDetails={$funcDetails.data.data} />
					{/if}
				{/key}
			</div>
		</div>
	</div>
</div>
