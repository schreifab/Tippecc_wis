<script lang="ts">
    let aoi: [number, number, number, number] = [0,0,0,0] //lat-min, lat-max,lon-min,lon-max
</script>
<div class = 'card'>
    <div class = 'card-body pb-3 pl-3' >
        aoi
        <label class="label">
            <input class="input" type="number" placeholder="lat-min" bind:value={aoi[0]}  />
            <input class="input" type="number" placeholder="lat-max" bind:value={aoi[1]}  />
            <input class="input" type="number" placeholder="lon-min" bind:value={aoi[2]}  />
            <input class="input" type="number" placeholder="lon-max" bind:value={aoi[3]}  />
        </label>
    </div>
</div>