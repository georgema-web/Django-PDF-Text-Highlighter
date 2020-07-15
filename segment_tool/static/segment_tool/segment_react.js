import React from 'react';


class ImageContainer extends React.Component {
    constructor(props) {
        super(props);
    }   
 
    render () {
        return (
            <div>
                <img src= {this.props.img_url} width="1200"> 
            </div>          
        );
    }
}


const domContainer = document.querySelector('#image_container'); 
console.log('running here');
ReactDOM.render(e(ImageContainer), domContainer); 
