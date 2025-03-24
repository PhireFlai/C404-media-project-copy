const parseId = (id) => {

    // Split the URL into parts and filter out empty strings
    const parts = id.split('/').filter(part => part !== '');

    // Get the last segment (the UUID)
    return parts[parts.length - 1];
}

export default parseId;
