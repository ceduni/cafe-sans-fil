import { ClockIcon,BellIcon, BellAlertIcon, HandThumbUpIcon} from "@heroicons/react/24/outline";

const NewsBoard = ({ news }) => {
    return (
      <div className="bg-white shadow rounded-lg p-4">
        <h2 className="text-lg font-bold text-gray-800 flex items-center mb-4">
          Annonces 
          <span className="ml-2 text-red-600 group">
                    <BellIcon className="h-5 w-5 flex-shrink-0 text-gray-400 group-hover:hidden mr-2" aria-hidden="true"/>
                    <BellAlertIcon className="h-5 w-5 flex-shrink-0 text-gray-400 hidden group-hover:block mr-2" aria-hidden="true"/>
                </span>
        </h2>
        {news.map((item, index) => (
          <div key={index} className="mb-4 last:mb-0">
            <div className="flex items-center justify-between">
              <h3 className="text-md font-semibold text-gray-900">{item.title}</h3>
              <span className="flex text-sm text-gray-500"><ClockIcon  className="h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-gray-500 mr-2"
                          aria-hidden="true"/>{item.timePosted}</span>
            </div>
            <p className="text-sm text-gray-600 mt-1">{item.content}</p>
            {/* Vérifier si tags est défini avant de le mapper */}
            {item.tags && item.tags.length > 0 && (
              <div className="flex items-center mt-2">
                {item.tags.map((tag, idx) => (
                  <span key={idx} className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded text-blue-600 bg-blue-200 last:mr-0 mr-1">
                    {tag}
                  </span>
                ))}
              </div>
            )}
            <div className="flex items-center justify-between mt-2">
              <button className="text-xs text-blue-600 border border-blue-600 rounded py-1 px-3 hover:bg-blue-600 hover:text-white transition-colors duration-300">
              
                {item.buttonText}
              </button>
              <span className="flex items-center text-gray-800">
                {/* <svg fill="currentColor" viewBox="0 0 20 20" className="w-4 h-4 mr-1"><path d="M2 5a2 2 0 011.757-1.974..."></path></svg> */}
                <HandThumbUpIcon className="h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-gray-500 mr-2"
                          aria-hidden="true"/>
                {item.likes}
              </span>
            </div>
          </div>
        ))}
      </div>
    );
  };
  
  export default NewsBoard;
  