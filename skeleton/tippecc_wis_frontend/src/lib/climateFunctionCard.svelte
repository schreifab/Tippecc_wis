<script lang="ts">
    import type {ClimateFunction} from "../ClimateFunction"
    export let climateFunction : ClimateFunction; 
</script>

<div class = 'card'>
    <header class = 'card-header flex justify-between items-center'><h2>{climateFunction.name}</h2>
        <button class = 'rounded p-2 variant-glass-primary'>&#8594;</button>
    </header>
    <div class = 'card-body pb-3 pl-3' >
        <p>
            {climateFunction.description}
        </p>
        
    </div>
</div>