<script lang="ts">
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import ClimateFunctions from '$lib/climateFunctions.svelte';

	const queryClient = new QueryClient();
</script>

<QueryClientProvider client={queryClient}>
	<ClimateFunctions />
</QueryClientProvider>
