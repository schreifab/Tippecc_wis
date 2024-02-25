export let aoi: [number, number, number, number] = [0, 0, 0, 0];
export function updateAoi(value: [number, number, number, number]) {
	aoi = value;
}
export let file_ids: string[] 
export function updateFileIds (fileIdDic: {name: string, count: number}[]){
	file_ids = []
	for (let file of fileIdDic){
		file_ids.push(file.name)
	}
}