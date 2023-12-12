<script lang="ts">
    import type {FunctionDetails, Dataset} from "$lib/interfaces";
    export let functionDetails : FunctionDetails; 

    import { popup } from '@skeletonlabs/skeleton';
    import type { PopupSettings } from '@skeletonlabs/skeleton';

    


    const popupHover: PopupSettings = {
	event: 'hover',
	target: 'popupHover',
	placement: 'bottom'
    };

</script>

<div class = 'card'>
    {#each functionDetails.datasets as dataset}
    <div>
        <p class = "[&>*]:pointer-events-none" use:popup={popupHover}>
            {dataset.name}
        </p>
        <div class="card p-4 variant-filled-secondary" data-popup="popupHover">
            <p>{dataset.desc}</p>
            <div class="arrow variant-filled-secondary" />
        </div>
    </div>
    {/each}
</div>