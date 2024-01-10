<script lang="ts">
    import {aoi} from "$lib/vars"
    import {updateAoi} from "$lib/vars"
    let aoiInput = aoi
    $: updateAoi(aoiInput)
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