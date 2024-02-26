export let aoi: [number, number, number, number] = [-35.97, -5.17, 10.01, 51.81];
export function updateAoi(value: [number, number, number, number]) {
	aoi = value;
}
export let file_ids: string[] 
export function updateFileIds (fileIdDic: {name: string, count: number}[]){
	file_ids = []
	for (let file of fileIdDic){
		file_ids.push(file.name)
	}
	console.log(file_ids)
}