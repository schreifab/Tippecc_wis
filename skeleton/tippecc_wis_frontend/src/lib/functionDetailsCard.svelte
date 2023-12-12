<script lang="ts">
    import type {FunctionDetails, Dataset, Parameter} from "$lib/interfaces";
    export let functionDetails : FunctionDetails; 

    import { popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';

    import { ListBox, ListBoxItem } from '@skeletonlabs/skeleton';

    function handleSubmit() {
        console.log(params_array_4_binding);
    }


    const popupHover: PopupSettings = {
	event: 'hover',
	target: 'popupHover',
	placement: 'bottom'
    };

    let data_list: String[] = ["TIPPECC_CLMcom-KIT-CCLM5-0-15_v1_MPI-M-MPI-ESM-LR_tas_day_1950_2100.nc"];
    let dataset_array_4_binding: {selection: string[], dataset: Dataset}[] = [];
    let params_array_4_binding: {selected_field: string | number, selected_unit: string, parameter: Parameter}[] = [];

    for (let ds of functionDetails.datasets) {
        dataset_array_4_binding.push({selection: [], dataset: ds});
    }

    for (let param of functionDetails.parameters) {
        params_array_4_binding.push({selected_field: "", selected_unit: "" , parameter: param});
    }
</script>

<div class = 'card'>
    {#each dataset_array_4_binding as entry}
    <div>
        <div class = "[&>*]:pointer-events-none" use:popup={popupHover}>
            {entry.dataset.name}
        </div>
        <div class="card p-4 variant-filled-secondary" data-popup="popupHover">
            <p>{entry.dataset.desc}</p>
            <div class="arrow variant-filled-secondary" />
        </div>
    
        <ListBox multiple>
            {#each data_list as data}
                <ListBoxItem bind:group={entry.selection} name="medium" value={data}>{data}</ListBoxItem>
            {/each}
        </ListBox>
    </div>
    {/each}
    {#each params_array_4_binding as entry}
    <div>
        <div class = "[&>*]:pointer-events-none" use:popup={popupHover}>
            {entry.parameter.name}
        </div>
        <div class="card p-4 variant-filled-secondary" data-popup="popupHover">
            <p>{entry.parameter.desc}</p>
            <div class="arrow variant-filled-secondary" />
        </div>
        {#if entry.parameter.input_list.length === 0}
            <label class="label">
                <input class="input" type="text" placeholder="Input" bind:value={entry.selected_field}  />
            </label>
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
    <button type="submit" on:click={handleSubmit}>submit</button>
</div>