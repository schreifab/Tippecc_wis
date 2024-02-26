<script lang="ts">
	import type {
		ClimateFunctionDetail,
		ClimateDataset,
		ClimateParameter,
		ClimateFunctionRequest
	} from '../model';
	export let functionDetails: ClimateFunctionDetail;

	import { popup } from '@skeletonlabs/skeleton';
	import type { PopupSettings } from '@skeletonlabs/skeleton';

	import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import { createApiClimateIndicesCreate, apiClimateIndicesCreate } from '../api/api';
	import { aoi, file_ids } from '$lib/vars';

	const api_post_request = createApiClimateIndicesCreate();
	let submitted: boolean = false;

	function handleSubmit(id: number) {
		let data_request: ClimateFunctionRequest;
		let dataset_array: string[] = []; 
		let params_dict: { [key: string]: string | number } = {};

		for (let entry of params_array_4_binding) {
			if (entry.selected_unit === '') {
				params_dict[entry.key] = entry.selected_field;
			} else {
				params_dict[entry.key] = entry.selected_field + ' ' + entry.selected_unit;
			}
		}

		for (let entry of dataset_array_4_binding) {
			if (entry.selection === true){
				dataset_array.push(entry.key)
			}
		}

		

		data_request = { aoi: aoi, dataset_list: dataset_array, file_id_list: file_ids,paramvalue_dict: params_dict };
		$api_post_request.mutate({ id: id, data: data_request });
		submitted = true;
	}

	const popupHover: PopupSettings = {
		event: 'hover',
		target: 'popupHover',
		placement: 'bottom'
	};

	function handle_popup(key:string){
		const popupHover: PopupSettings = {
		event: 'hover',
		target: 'popover'+key,
		placement: 'bottom'
	}
	return popupHover
	}

	let dataset_array_4_binding: { selection: Boolean; key: string; dataset: ClimateDataset }[] = [];
	let params_array_4_binding: {
		key: string;
		selected_field: string | number;
		selected_unit: string;
		parameter: ClimateParameter;
	}[] = [];

	for (let key in functionDetails.dataset_dict) {
		dataset_array_4_binding.push({
			selection: true,
			key: key,
			dataset: functionDetails.dataset_dict[key]
		});
	}

	for (let key in functionDetails.params_dict) {
		params_array_4_binding.push({
			key: key,
			selected_field: '',
			selected_unit: '',
			parameter: functionDetails.params_dict[key]
		});
	}
</script>

<div class="card pb-3 pl-3 pr-3 pt-2">
	<div class="card p-2 variant-filled-surface">Datasets</div>

	{#each dataset_array_4_binding as entry}
		<div>
			<div>
				<!--class = "[&>*]:pointer-events-none" use:popup={popupHover}>-->
				<span data-popover-target ="popover{entry.key}" class="badge variant-ghost [&>*]:pointer-events-none" use:popup={handle_popup(entry.key)}>
					{entry.dataset.name}
				</span>
			</div>
			<div class="card p-4 variant-filled-secondary" data-popup="popover{entry.key}">
				<p>{entry.dataset.desc}</p>
				<div class="arrow variant-filled-secondary" />
			</div>
			{#if entry.dataset.optional === false}
				<div class="flex items-center">
					<input
						disabled
						checked
						id="disabled-checked-checkbox"
						type="checkbox"
						bind:value={entry.selection}
						class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
					/>
					<label
						for="disabled-checked-checkbox"
						class="ms-2 text-sm font-medium text-gray-400 dark:text-gray-500">{entry.key}</label
					>
				</div>
			{:else}
				hello
				<div class="flex items-center">
					<input
						checked
						id="disabled-checked-checkbox"
						type="checkbox"
						bind:value={entry.selection}
						class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
					/>
					<label
						for="disabled-checked-checkbox"
						class="ms-2 text-sm font-medium text-gray-400 dark:text-gray-500">{entry.key}</label
					>
				</div>
			{/if}
		</div>
	{/each}
	<br />
	<div class="card p-2 variant-filled-surface">Parameters</div>
	{#each params_array_4_binding as entry}
		<div>
			<div>
				<!--class = "[&>*]:pointer-events-none" use:popup={popupHover}>-->
				<span data-popover-target ="popover{entry.key}" class="badge variant-ghost [&>*]:pointer-events-none" use:popup={handle_popup(entry.key)}>
					{entry.parameter.name}
				</span>
			</div>
			<div class="card p-4 variant-filled-secondary" data-popup="popover{entry.key}">
				<p>{entry.parameter.desc}</p>
				<div class="arrow variant-filled-secondary" />
			</div>
			{#if entry.parameter.input_list.length === 0}
				{#if entry.parameter.datatype === "String" || entry.parameter.datatype === "str"}
					<label class="label">
						<input class="input" type="text" placeholder="Input" bind:value={entry.selected_field} />
					</label>
				{/if}
				{#if entry.parameter.datatype === "number" || entry.parameter.datatype === "quantified" || entry.parameter.datatype === "float" || entry.parameter.datatype === "double"}
					<label class="label">
						<input class="input" type="number" step="0.001" placeholder="Input" bind:value={entry.selected_field} />
					</label>
				{/if}
				{#if entry.parameter.datatype === "int" || entry.parameter.datatype === "Integer"}
					<label class="label">
						<input class="input" type="number" step="1" placeholder="Input" bind:value={entry.selected_field} />
					</label>
				{/if}
			{:else}
				<ListBox>
					{#each entry.parameter.input_list as input_option}
						<ListBoxItem bind:group={entry.selected_field} name="medium" value={input_option}
							>{input_option}</ListBoxItem
						>
					{/each}
				</ListBox>
			{/if}
			{#if entry.parameter.unit_list.length !== 0}
				<label class="label">
					<select class="select" bind:value={entry.selected_unit}>
						{#each entry.parameter.unit_list as unit}
							<option value={unit}>{unit}</option>
						{/each}
					</select>
				</label>
			{/if}
		</div>
	{/each}
	<br />

	<button
		type="submit"
		class="btn variant-filled-surface"
		on:click={() => handleSubmit(functionDetails.id)}>submit</button
	>
</div>

<br />
{#if submitted}
	<div class="card">
		<header class="card-header flex justify-between items-center">
			<h2>Data submitted</h2>
		</header>
		<div class="card-body pb-3 pl-3">
			<p>
				{#if $api_post_request.data}
					{$api_post_request.data?.data.message}
				{:else}
					execution in progress
				{/if}
			</p>
		</div>
	</div>
{/if}
